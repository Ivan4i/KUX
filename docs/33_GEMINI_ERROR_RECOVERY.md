# 33_GEMINI_ERROR_RECOVERY.md

## Error Handling & Recovery Strategies

### Error Categories

| Категория | Примеры ошибок | Recovery | Priority |
|-----------|-------------|----------|----------|
| **Cache Errors** | Cache expired, not found, corrupted | Recreate cache | HIGH |
| **Rate Limit** | 429 Too Many Requests | Exponential backoff, queue | HIGH |
| **API Timeout** | Request timeout (>30s), connection reset | Retry with increased timeout | HIGH |
| **Output Quality** | Generated text too short, missing elements | Regenerate with stricter prompt | MEDIUM |
| **Validation Errors** | Failed validation checks | Retry with adjusted constraints | MEDIUM |
| **Data Quality** | Bad RusProfile data, missing fields | Use defaults, skip or notify | LOW |

---

## Tier 1: Auto-Recovery (Device/Service Handles Locally)

### Strategy 1A: Cache Recreation on Expiry

```python
def handle_cache_expired():
    """
    Tier 1 Auto-Recovery
    
    When: Cache TTL exceeded (24 hours passed)
    What: Recreate cache from .md files
    Cost: $0.13 (one-time), worth it for fresh context
    """
    
    print("⏰ Cache expired, recreating...")
    
    try:
        # Reload .md files
        context_pack = load_context_files()
        
        # Recreate cache
        new_cache = client.caches.create(
            model="gemini-3-pro",
            config={
                "display_name": "business-analysis-context-pack",
                "contents": [{"parts": [{"text": combined_context}]}]
            }
        )
        
        # Update global cache reference
        GLOBAL_CACHE["name"] = new_cache.name
        GLOBAL_CACHE["created_at"] = datetime.now()
        GLOBAL_CACHE["expires_at"] = datetime.now() + timedelta(hours=24)
        
        print(f"✓ Cache recreated: {new_cache.name}")
        return True
        
    except Exception as e:
        print(f"✗ Cache recreation failed: {e}")
        return False
```

### Strategy 1B: Retry with Variance (Timeout/Connection)

```python
def handle_api_timeout_with_retry():
    """
    Tier 1 Auto-Recovery
    
    When: API request times out (>30 seconds)
    What: Retry with increased timeout and backoff
    Logic:
      - Attempt 1: 30s timeout
      - Attempt 2: 60s timeout (wait 5s first)
      - Attempt 3: 90s timeout (wait 15s first)
      - Attempt 4: Give up, escalate to Tier 2
    """
    
    max_attempts = 3
    base_timeout = 30
    
    for attempt in range(1, max_attempts + 1):
        timeout = base_timeout + (attempt - 1) * 30
        
        # Wait before retry (exponential: 0s, 5s, 15s)
        if attempt > 1:
            wait_time = (attempt - 2) * 10 + 5
            print(f"⏸️  Waiting {wait_time}s before retry #{attempt}...")
            time.sleep(wait_time)
        
        try:
            print(f"🔄 Attempt #{attempt} (timeout: {timeout}s)...")
            
            response = client.models.generate_content(
                model="gemini-3-pro",
                contents=prompt,
                config={
                    "cached_content": GLOBAL_CACHE["name"],
                    "timeout": timeout,
                }
            )
            
            print(f"✓ Success on attempt {attempt}")
            return response
            
        except TimeoutError as e:
            print(f"⏱️  Timeout on attempt {attempt}: {e}")
            
            if attempt == max_attempts:
                print(f"✗ Failed after {max_attempts} attempts")
                return None
    
    return None
```

### Strategy 1C: Regenerate with Stricter Prompt (Quality Issue)

```python
def handle_output_validation_failure(
    generated_text: str,
    input_data: dict,
    attempt: int = 1
) -> str | None:
    """
    Tier 1 Auto-Recovery
    
    When: Generated message fails validation (too short, missing elements)
    What: Regenerate with stricter constraints
    Max attempts: 3
    """
    
    max_attempts = 3
    
    # Validate
    validation = validate_gemini_output(generated_text, input_data)
    
    if validation["valid"]:
        print(f"✓ Output valid (attempt {attempt})")
        return generated_text
    
    if attempt >= max_attempts:
        print(f"✗ Output validation failed after {max_attempts} attempts")
        print(f"  Errors: {validation['errors']}")
        return None  # Escalate to Tier 2
    
    # Regenerate with stricter constraints
    print(f"⚠️  Output validation failed (attempt {attempt}/{max_attempts})")
    print(f"  Issues: {validation['errors']}")
    
    stricter_prompt = f"""
    {ORIGINAL_PROMPT}
    
    ⚠️  ВАЖНО: Предыдущий ответ имел эти ошибки:
    {', '.join(validation['errors'])}
    
    ИСПРАВЬ эти ошибки в новом ответе:
    1. {validation['errors'][0] if validation['errors'] else 'Format correctly'}
    2. Убедись что текст 100-150 слов
    3. Упомяни ВСЕ обязательные элементы
    
    ВЫВЕДИ ТОЛЬКО ИСПРАВЛЕННОЕ СООБЩЕНИЕ.
    """
    
    print(f"🔄 Regenerating with stricter constraints...")
    
    new_output = client.models.generate_content(
        model="gemini-3-pro",
        contents=stricter_prompt,
        config={
            "cached_content": GLOBAL_CACHE["name"],
            "temperature": 0.6,  # More deterministic
            "top_p": 0.85,
        }
    ).text.strip()
    
    # Recursive retry
    return handle_output_validation_failure(new_output, input_data, attempt + 1)
```

---

## Tier 2: Fallback Strategies (Alternative Approaches)

### Strategy 2A: Use Implicit Caching (Explicit Failed)

```python
def fallback_to_implicit_caching():
    """
    Tier 2 Fallback
    
    When: Explicit cache failed (creation error, not found, etc)
    What: Use implicit caching (automatic, slower but works)
    
    How implicit works:
    - Send full context + prompt to Gemini
    - Gemini auto-caches repeated prefixes
    - Reuse cache on next request (if prefix is same)
    - Cost: Slightly higher (no explicit discount) but still works
    """
    
    print("⚠️  Explicit cache failed, using implicit caching fallback...")
    
    # Load context again (no cache reference)
    context_pack = load_context_files()
    combined_context = combine_context_files(context_pack)
    
    # Send WITH context (no cached_content parameter)
    response = client.models.generate_content(
        model="gemini-3-pro",
        contents=[
            {
                "parts": [{"text": combined_context}]  # Full content, no cache
            },
            {
                "parts": [{"text": prompt}]  # Prompt
            }
        ],
        config={
            "temperature": 0.7,
            "top_p": 0.9,
        }
    )
    
    print("✓ Using implicit caching (slower but functional)")
    return response
```

### Strategy 2B: Use Fallback Template (Generation Failed)

```python
def fallback_to_template(company_name: str, founder_name: str, business_data: dict) -> str:
    """
    Tier 2 Fallback
    
    When: Gemini generation failed 3+ times
    What: Use generic but solid template
    Cost: $0 (no API call)
    Quality: 70-80% of Gemini quality (still professional)
    
    Template approach:
    - Pre-written templates with variable substitution
    - Fast, reliable, no API dependencies
    - Use as last resort (when Gemini unreachable)
    """
    
    print(f"⚠️  Fallback to template for {company_name}...")
    
    founder_first = founder_name.split()[0]
    revenue_millions = business_data["revenue_2024"] / 1_000_000
    employees = business_data["employees"]
    
    templates = [
        f"""{founder_first}, видно что "{company_name}" развивается 
(выручка {revenue_millions:.0f} млн, {employees} человек). Сейчас рыночное окно — 
компании активно цифровизируются. Чаще всего боль в неавтоматизированных процессах. 
Давайте встретимся завтра в 10:30 или 14:00 обсудить вашу ситуацию. https://t.me/grigory_ux""",
        
        f"""{founder_first}, вижу "{company_name}" на RusProfile с {employees} сотрудниками 
и выручкой {revenue_millions:.0f} млн руб. — это серьезный бизнес. Интересно узнать, 
как вы видите возможности роста? Обсудим завтра — 11:00 или 15:00? 
https://t.me/grigory_ux Сам предприниматель с автоматизированными проектами.""",
    ]
    
    # Select random template
    message = random.choice(templates)
    
    return {
        "message": message,
        "source": "fallback_template",
        "quality": "medium",
        "warning": "⚠️  Using template, not Gemini-generated"
    }
```

### Strategy 2C: Queue for Retry Later (Rate Limit Hit)

```python
def fallback_queue_for_retry(company_id: str, reason: str):
    """
    Tier 2 Fallback
    
    When: Rate limit hit (429 Too Many Requests)
    What: Queue task for retry in 5-10 minutes
    Logic:
      - Don't lose the task
      - Try again when rate limit resets
      - Continue with other companies meanwhile
    """
    
    print(f"⏳ Rate limited, queuing for retry: {company_id}")
    
    retry_task = {
        "company_id": company_id,
        "status": "rate_limit_queue",
        "reason": reason,
        "queued_at": datetime.now(),
        "retry_after": datetime.now() + timedelta(minutes=5),
        "attempt_count": 1,
    }
    
    # Add to Celery queue or in-memory queue
    RETRY_QUEUE.append(retry_task)
    
    # Log for monitoring
    print(f"✓ Queued for retry at {retry_task['retry_after']}")
    
    # Continue with next task
    return None
```

---

## Tier 3: Escalation (Manual Intervention Required)

### When to Escalate

```python
def should_escalate(error: Exception, attempt_count: int) -> bool:
    """
    Determine if error should escalate to manual intervention.
    
    Escalate when:
    1. Tier 1 & 2 failed (all recovery attempts exhausted)
    2. Unrecoverable error (account banned, API down)
    3. Too many attempts (>3 times same error)
    4. Unknown error (can't diagnose)
    """
    
    # Tier 1 & 2 exhausted
    if attempt_count > 5:
        return True
    
    # Unrecoverable errors
    unrecoverable = [
        "Invalid API key",
        "Account suspended",
        "Service temporarily unavailable",
        "Authentication failed",
    ]
    
    for msg in unrecoverable:
        if msg in str(error):
            return True
    
    # Unknown error (can't diagnose)
    if not any(known_type in type(error).__name__ for known_type in [
        "TimeoutError", "RateLimitError", "ValidationError"
    ]):
        return True
    
    return False
```

### Escalation Handler

```python
def escalate_to_manual_review(
    company_id: str,
    company_data: dict,
    error_context: dict
) -> None:
    """
    Tier 3 Escalation
    
    Steps:
    1. Capture full error context
    2. Create admin task
    3. Send notification
    4. Await human decision
    """
    
    escalation_ticket = {
        "id": f"ESC-{datetime.now().strftime('%Y%m%d%H%M%S')}-{company_id}",
        "status": "pending_review",
        "company_id": company_id,
        "company_name": company_data.get("company_name"),
        "created_at": datetime.now(),
        
        # Full context for admin
        "context": {
            "company_data": company_data,
            "error_type": error_context.get("error_type"),
            "error_message": error_context.get("error_message"),
            "attempts": error_context.get("attempt_count"),
            "screenshots": error_context.get("screenshots", []),
        },
        
        "recommended_action": error_context.get("recommendation", "Review and decide"),
    }
    
    # Store ticket
    ESCALATION_DB.insert(escalation_ticket)
    
    # Send notification
    send_slack_notification({
        "channel": "#ai-agents",
        "text": f"🔴 Escalation needed: {company_data['company_name']} (attempt #{error_context['attempt_count']})",
        "ticket_id": escalation_ticket["id"],
        "action_url": f"https://admin.dashboard/escalations/{escalation_ticket['id']}",
    })
    
    # Email admin
    send_email({
        "to": "admin@company.com",
        "subject": f"Manual review needed: {company_data['company_name']}",
        "body": f"""
        Company: {company_data['company_name']}
        Error: {error_context.get('error_message')}
        
        Review ticket: {escalation_ticket['id']}
        """
    })
    
    print(f"✓ Escalated to manual review: {escalation_ticket['id']}")
```

---

## Complete Recovery Decision Tree

```
REQUEST TO GEMINI
  ↓
Is cache valid?
├─ NO → Handle Cache Error
│   ├─ Tier 1: Recreate cache
│   │   ├─ Success → Use new cache
│   │   └─ Failure → Next
│   ├─ Tier 2: Use implicit caching
│   │   ├─ Success → Continue (slower)
│   │   └─ Failure → Next
│   └─ Tier 3: Escalate
│
├─ YES → Send request
    ↓
Got response?
├─ NO (Timeout/Error)
│   ├─ Tier 1: Retry with increased timeout
│   │   ├─ Success → Continue
│   │   └─ Failure → Next
│   ├─ Tier 2: Queue for later
│   │   └─ Continue with next task
│   └─ Tier 3: Escalate if rate_limit > 3
│
├─ YES → Got text
    ↓
Output valid?
├─ NO (Validation failed)
│   ├─ Tier 1: Regenerate with stricter prompt (3 attempts)
│   │   ├─ Success → Use new output
│   │   └─ Failure → Next
│   ├─ Tier 2: Use fallback template
│   │   └─ Return template message
│   └─ Tier 3: Escalate for review
│
└─ YES → Success! Use message
```

---

## Monitoring & Alerting

### Error Metrics to Track

```python
ERROR_METRICS = {
    "cache_recreations": {
        "count": 0,
        "last_time": None,
        "threshold_alert": ">2 in 1 hour",
    },
    "api_timeouts": {
        "count": 0,
        "last_time": None,
        "threshold_alert": ">5 in 1 hour",
    },
    "rate_limits": {
        "count": 0,
        "last_time": None,
        "threshold_alert": ">3 in 1 hour",
    },
    "validation_failures": {
        "count": 0,
        "last_time": None,
        "threshold_alert": ">10 in 1 hour",
    },
    "escalations": {
        "count": 0,
        "last_time": None,
        "threshold_alert": "Any escalation",
    },
}

def monitor_error_metrics():
    """
    Check error metrics every 5 minutes.
    Send alerts if thresholds exceeded.
    """
    
    for error_type, metrics in ERROR_METRICS.items():
        if metrics["count"] > 0:
            
            # Check if threshold met
            threshold = int(metrics["threshold_alert"].split(">")[1].split(" ")[0])
            time_window = metrics["threshold_alert"].split()[-1]
            
            if metrics["count"] > threshold:
                send_alert({
                    "severity": "HIGH" if error_type == "escalations" else "MEDIUM",
                    "error_type": error_type,
                    "count": metrics["count"],
                    "time_window": time_window,
                    "recommendation": get_recommendation(error_type),
                })
```

### Alert Recommendations

```python
ALERT_RECOMMENDATIONS = {
    "cache_recreations": "Cache recreating too often. Check if .md files changing frequently.",
    "api_timeouts": "Gemini API slow. Check status page, consider increasing timeout.",
    "rate_limits": "Hit rate limit. Implement queue-based batching instead of parallel.",
    "validation_failures": "Output quality low. Check prompt clarity or Gemini context.",
    "escalations": "Manual intervention needed. Review escalation tickets.",
}
```

---

## Testing Recovery Flows

### Test Scenarios

```
✅ TEST 1: Cache Expiration
- Create cache with TTL 1 minute
- Wait 65 seconds
- Call generate_content()
- Expected: Auto-recreate cache, succeed

✅ TEST 2: Timeout Recovery
- Mock API to timeout
- Call generate_content()
- Expected: Retry 3 times with increased timeout, then escalate

✅ TEST 3: Output Validation Failure
- Mock Gemini to return too-short text
- Call validate_output()
- Expected: Regenerate with stricter prompt, succeed on attempt 2-3

✅ TEST 4: Rate Limit Fallback
- Mock API 429 error
- Call generate_content()
- Expected: Queue for retry, return None, continue with next

✅ TEST 5: Complete Failure → Escalation
- Mock all Tier 1 & 2 to fail
- Call generate_content()
- Expected: Create escalation ticket, send notification
```

---

## End of 33_GEMINI_ERROR_RECOVERY.md