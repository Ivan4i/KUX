# ⚠️ NOTION ERROR HANDLING: Recovery & Mitigation

## Error Classification & Response

### Tier 1: Auth Errors (Don't Retry)

**401 Unauthorized**
```
Cause: API key invalid, expired, or doesn't have permission

Detection:
  response.status_code == 401

Response:
  • Log error immediately
  • Stop all Notion API calls
  • Notify user in Telegram:
    "❌ Notion API key invalid or expired. Check .env"
  • Disable Notion sync
  
Fix:
  1. User verifies API key in Notion dashboard
  2. Regenerate key if needed
  3. Update .env file
  4. Restart backend
  5. Admin manually re-enables sync
```

**403 Forbidden**
```
Cause: Integration doesn't have permission to access database

Detection:
  response.status_code == 403

Response:
  • Log error immediately
  • Stop sync for this database
  • Notify user:
    "❌ Integration not authorized for this database.
     Grant access in Notion: Databases → Share → Select integration"
  
Fix:
  1. User goes to Notion database
  2. Click "Share" → "Add"
  3. Select "Automation Sync" integration
  4. Restart backend
```

**404 Not Found**
```
Cause: Database ID is wrong or database was deleted

Detection:
  response.status_code == 404
  AND endpoint is /databases/{database_id}

Response:
  • Log error
  • Notify user:
    "❌ Database not found. Check database ID in config."
  • Disable this sync
  
Fix:
  1. User verifies database ID (copy from Notion share link)
  2. Update config.py or .env
  3. Restart backend
```

### Tier 2: Rate Limiting (Exponential Backoff)

**429 Too Many Requests**
```
Cause: Hit API rate limit (3 requests/second)

Detection:
  response.status_code == 429
  response.headers.get("Retry-After")

Response:
  • WAIT (don't retry immediately)
  • Extract Retry-After header (usually 30-60 sec)
  • Queue request for later
  • Log warning (not error)
  
Implementation:
  if response.status_code == 429:
      retry_after = int(response.headers.get("Retry-After", 30))
      logger.warning(f"Rate limited, waiting {retry_after} sec")
      await asyncio.sleep(retry_after)
      # Retry the SAME request (max 3 times)
```

**Rate Limit Safety**

```python
class RateLimitProtection:
    def __init__(self):
        self.request_count = 0
        self.window_start = time.time()
        self.max_requests_per_second = 2  # Our limit (leave margin for others)
        
    async def acquire(self):
        """Wait if needed to respect rate limits"""
        
        now = time.time()
        elapsed = now - self.window_start
        
        if elapsed >= 1.0:
            # New window
            self.request_count = 0
            self.window_start = now
        
        if self.request_count >= self.max_requests_per_second:
            # Wait for next window
            sleep_time = 1.0 - elapsed
            logger.debug(f"Rate limit: waiting {sleep_time:.2f} sec")
            await asyncio.sleep(sleep_time)
            self.request_count = 0
            self.window_start = time.time()
        
        self.request_count += 1
        return True

# Usage
rate_limiter = RateLimitProtection()

async def api_call():
    await rate_limiter.acquire()
    # Make request
```

### Tier 3: Transient Errors (Retry with Backoff)

**500-599 Server Errors**
```
Cause: Notion server issue (temporary)

Detection:
  response.status_code >= 500

Response:
  • Retry with exponential backoff
  • Max 3 retries
  • Delays: 1 sec, 2 sec, 4 sec
  
Implementation:
  for attempt in range(3):
      try:
          response = requests.get(url, timeout=30)
          if response.status_code >= 500:
              raise ServerError(response.status_code)
          return response
      except ServerError:
          if attempt < 2:
              wait = 2 ** attempt
              logger.warning(f"Server error, retry in {wait} sec")
              await asyncio.sleep(wait)
          else:
              raise
```

**Request Timeout**
```
Cause: Network slow, Notion slow, or hung connection

Detection:
  requests.Timeout exception
  OR response.status_code == 504 (Gateway Timeout)

Response:
  • Retry up to 3 times
  • Exponential backoff: 1, 2, 4 sec
  • Fall back to cache on final failure
  
Implementation:
  for attempt in range(3):
      try:
          response = requests.get(url, timeout=30)
          return response
      except requests.Timeout:
          if attempt < 2:
              wait = 2 ** attempt
              logger.warning(f"Timeout, retry {attempt+1}/3")
              await asyncio.sleep(wait)
          else:
              logger.error("Max retries exceeded")
              return use_cache()
```

### Tier 4: Data Errors (Skip & Log)

**Invalid Response Format**
```
Cause: Notion API changed format or response corrupted

Detection:
  KeyError, IndexError, or TypeError during parsing

Response:
  • Log error with full response
  • Skip this contact
  • Continue with next
  • Don't crash sync
  
Implementation:
  def parse_contact(page: dict) -> Optional[dict]:
      try:
          return {
              "name": page["properties"]["Full Name"]["title"][0]["text"]["content"],
              ...
          }
      except (KeyError, IndexError, TypeError) as e:
          logger.error(f"Parse error for {page.get('id')}: {e}")
          logger.debug(f"Raw page: {page}")
          return None  # Skip this contact
```

**Missing Required Fields**
```
Cause: User didn't fill in required Notion fields

Detection:
  Parse returns None or empty string for required field

Response:
  • Skip this contact
  • Log warning (not error)
  • Continue with next
  
Implementation:
  if not contact.get("phone"):
      logger.warning(f"Contact '{contact.get('name')}' has no phone, skipping")
      continue
```

---

## Complete Error Handler

```python
class NotionErrorHandler:
    
    # Error categories
    AUTH_ERRORS = [401, 403, 404]
    RATE_LIMIT_ERRORS = [429]
    SERVER_ERRORS = [500, 502, 503, 504]
    TRANSIENT_ERRORS = SERVER_ERRORS + [408]  # 408 = Request Timeout
    
    def __init__(self):
        self.last_auth_error_time = None
        self.consecutive_failures = 0
        self.max_consecutive_failures = 5
        
    async def handle_response(self, response: requests.Response, operation: str):
        """Handle API response, return data or raise exception"""
        
        status = response.status_code
        
        # Success
        if 200 <= status < 300:
            self.consecutive_failures = 0
            return response.json()
        
        # Auth error - fatal
        if status in self.AUTH_ERRORS:
            logger.critical(f"Auth error {status}: {response.text}")
            self.last_auth_error_time = datetime.now()
            raise NotionAuthError(f"Auth failed: {status}")
        
        # Rate limit - wait and retry
        if status in self.RATE_LIMIT_ERRORS:
            retry_after = int(response.headers.get("Retry-After", 30))
            logger.warning(f"Rate limited, waiting {retry_after} sec")
            await asyncio.sleep(retry_after)
            # Request will be retried by caller
            raise NotionRateLimitError(retry_after)
        
        # Server error - retry
        if status in self.SERVER_ERRORS:
            logger.warning(f"Server error {status}, will retry")
            self.consecutive_failures += 1
            if self.consecutive_failures > self.max_consecutive_failures:
                logger.error("Max consecutive failures, pausing sync")
                raise NotionOutageError("Too many server errors")
            raise NotionServerError(status)
        
        # Unknown error
        logger.error(f"Unexpected status {status}: {response.text}")
        raise NotionAPIError(f"Unknown error: {status}")

    async def execute_with_retry(
        self,
        operation: str,
        func,
        *args,
        max_retries: int = 3,
        **kwargs
    ):
        """Execute operation with retry logic"""
        
        handler = NotionErrorHandler()
        
        for attempt in range(max_retries):
            try:
                return await func(*args, **kwargs)
                
            except NotionAuthError:
                # Fatal - don't retry
                raise
                
            except NotionRateLimitError as e:
                # Already waited, retry immediately
                await asyncio.sleep(0.5)
                continue
                
            except NotionServerError:
                if attempt < max_retries - 1:
                    wait = 2 ** attempt
                    logger.warning(f"Retry {attempt+1}/{max_retries} in {wait} sec")
                    await asyncio.sleep(wait)
                else:
                    raise
                    
            except Exception as e:
                logger.error(f"Operation failed: {e}")
                raise
        
        raise NotionAPIError(f"Failed after {max_retries} retries")
```

---

## Graceful Degradation

### Notion Completely Down

```python
async def sync_with_fallback():
    """Fetch from Notion, fallback to cache if down"""
    
    try:
        contacts = await fetch_new_contacts()
        cache.save(contacts)
        return contacts
        
    except NotionAuthError:
        # Auth error - fatal, don't retry
        logger.critical("Notion auth failed, sync disabled")
        await notify_user("Notion authentication failed")
        return []  # No contacts to process
        
    except NotionOutageError:
        # Notion server down - use cache
        logger.warning("Notion appears down, using cached contacts")
        cached = cache.load()
        if cached:
            await notify_user("⚠️ Using cached contacts (Notion may be down)")
            return cached
        else:
            logger.error("No cache available, cannot sync")
            return []
```

### Dashboard Indicator

```
Display to user:

Notion Status: 🟢 Connected
  Last sync: 2 minutes ago
  Contacts fetched: 45
  Pending contacts: 12
  
  [Last sync was from cache] ← Show if using cache
```

---

## Monitoring & Alerts

### Error Tracking

```python
class NotionErrorMetrics:
    def __init__(self):
        self.errors = defaultdict(int)
        self.last_error_time = None
        self.last_success_time = None
        
    def record_error(self, error_type: str):
        """Track error frequency"""
        self.errors[error_type] += 1
        self.last_error_time = datetime.now()
        
    def record_success(self):
        """Track successful sync"""
        self.last_success_time = datetime.now()
        
    def get_health(self) -> dict:
        """Return health status"""
        
        if not self.last_success_time:
            return {"status": "unknown", "reason": "Never synced"}
        
        time_since_success = datetime.now() - self.last_success_time
        
        if time_since_success.total_seconds() > 3600:  # > 1 hour
            return {"status": "unhealthy", "reason": "No sync in 1+ hours"}
        
        if time_since_success.total_seconds() > 300:  # > 5 min
            return {"status": "degraded", "reason": "Last sync > 5 min ago"}
        
        return {"status": "healthy", "last_sync": self.last_success_time}
```

### Alert Conditions

```
🔴 CRITICAL:
  • Auth error (401/403) → Immediate manual action required
  • No successful sync in 2+ hours → System disabled

🟠 WARNING:
  • 5+ consecutive server errors → May need intervention
  • Using cache for > 30 min → Notion may be down
  • Rate limit hits > 1/day → May need API key rotation

🟡 INFO:
  • Rate limit hit → Normal, handled by exponential backoff
  • Single retry needed → Normal, transient issue
  • Parse error on one contact → Skip and continue
```

---

## End of 23_NOTION_ERROR_HANDLING.md

Полная стратегия обработки ошибок Notion.

---

## 📊 РАЗДЕЛ C ЗАВЕРШЁН!

**4 файла созданы:**
1. ✅ 20_NOTION_CRM_SYNC.md
2. ✅ 21_NOTION_API_INTEGRATION.md
3. ✅ 22_NOTION_WEBHOOK_HANDLER.md
4. ✅ 23_NOTION_ERROR_HANDLING.md

**Всего файлов: 12 / 41**

```
РАЗДЕЛ A (Мастер-концепция): ✅ 3/3
РАЗДЕЛ B (Архитектура): ✅ 5/5
РАЗДЕЛ C (Notion): ✅ 4/4

РАЗДЕЛ D (Gemini LLM): ⏳ 0/4
РАЗДЕЛ E (Android): ⏳ 0/6
РАЗДЕЛ F (Frontend): ⏳ 0/5
РАЗДЕЛ G (Backend): ⏳ 0/6
РАЗДЕЛ H (Workflows): ⏳ 0/4
РАЗДЕЛ I (Database): ⏳ 0/3
```

**Продолжить РАЗДЕЛ D (Gemini LLM Integration)?** 🚀
