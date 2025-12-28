# 📋 NOTION CRM SYNC: Complete Integration Strategy

## Overview

### Data Flow: Notion ← → SQLite Local DB ← → Backend

```
User in Notion:
  • Adds/edits contacts (name, phone, company)
  • Sets status (pending, sent, confirmed)
  • Reviews messages (message_sent field)

↓ (Notion API Polling)

Backend polling service (NotionSync):
  • Every 1 minute: fetch new/updated rows
  • Parse phone numbers, company data
  • Store in local SQLite
  • Create tasks for new contacts

↓ (Task Execution)

Device agents execute:
  • Send message to phone number
  • Update task status (sent, failed)
  • Take screenshot (proof)

↓ (Sync back to Notion)

NotionSync.update_status():
  • Update Notion row: status='sent'
  • Update Notion row: message_sent={text}
  • Update Notion row: response_date={today}
```

---

## Notion Database Schema (Contacts Table)

### Columns Required

| Column | Type | Example | Purpose |
|--------|------|---------|---------|
| **ID** | Unique ID | `notion_abc123` | Primary key |
| **Full Name** | Text | `Иван Петров` | For personalization |
| **Phone** | Phone/Text | `+7-999-123-45-67` | Send destination |
| **Company** | Text | `ООО ТДБаза` | Context for Gemini |
| **Website** | URL | `https://example.ru` | Optional context |
| **RusProfile URL** | URL | `https://rusprofile.ru/id/123456` | Research source |
| **Revenue (RUB)** | Number | `7000000` | For Gemini context |
| **Profit (RUB)** | Number | `500000` | For Gemini context |
| **Status** | Select | `pending` | Workflow status |
| **Sent via MAX** | Checkbox | ☑ | Has message been sent? |
| **Sent via SMS** | Checkbox | ☐ | Has SMS been sent? |
| **Sent via WhatsApp** | Checkbox | ☐ | Has WA been sent? |
| **Last Message** | Text (long) | `"Иван, видел выручка..."` | Message content sent |
| **Response** | Text | `"Спасибо, интересно!"` | If they replied |
| **Response Date** | Date | `2025-01-27` | When they replied |
| **Notes** | Text | `"Follow up next week"` | Internal notes |
| **Created Date** | Created time | `2025-01-20 10:15` | Auto timestamp |
| **Last Updated** | Last edited time | `2025-01-27 14:30` | Auto timestamp |

### Status Select Options

```
pending    → New contact, not contacted yet
processing → Currently executing (sending message)
sent       → Message sent successfully
failed     → Message send failed (error)
confirmed  → Contact replied / interested
paused     → Temporarily paused (don't send)
archived   → Don't contact anymore (opt-out)
```

---

## Notion API Integration Points

### 1. Fetch New Contacts (Polling)

**Endpoint:** `GET /v1/databases/{database_id}/query`

**Query Strategy:**

```python
# Every 1 minute (max 60/hour, well under Notion limit of 3/sec)

# Fetch only NEW or UPDATED rows:
filter = {
  "and": [
    {
      "property": "Status",
      "select": {
        "equals": "pending"  # Only pending contacts
      }
    },
    {
      "property": "Last Updated",
      "date": {
        "after": last_sync_time  # Only since last sync
      }
    }
  ]
}

# Request:
POST https://api.notion.com/v1/databases/{database_id}/query
Headers:
  Authorization: Bearer {NOTION_API_KEY}
  Notion-Version: 2022-06-28
Body:
  {
    "filter": filter,
    "page_size": 50,  # Fetch 50 at a time
    "sorts": [
      {
        "property": "Created Date",
        "direction": "ascending"
      }
    ]
  }
```

**Response Parsing:**

```python
{
  "results": [
    {
      "id": "abc123def456",
      "properties": {
        "Full Name": {
          "title": [{"text": {"content": "Иван Петров"}}]
        },
        "Phone": {
          "phone_number": "+7-999-123-45-67"
        },
        "Company": {
          "rich_text": [{"text": {"content": "ООО ТДБаза"}}]
        },
        "Revenue (RUB)": {
          "number": 7000000
        },
        "Status": {
          "select": {"name": "pending"}
        }
      }
    }
  ],
  "has_more": false,
  "next_cursor": null
}
```

**Python Implementation:**

```python
def fetch_new_contacts(database_id: str, last_sync: datetime) -> List[dict]:
    """Fetch pending contacts from Notion"""
    
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28"
    }
    
    payload = {
        "filter": {
            "and": [
                {
                    "property": "Status",
                    "select": {"equals": "pending"}
                },
                {
                    "property": "Last Updated",
                    "date": {"after": last_sync.isoformat()}
                }
            ]
        },
        "page_size": 50,
        "sorts": [{"property": "Created Date", "direction": "ascending"}]
    }
    
    response = requests.post(
        f"https://api.notion.com/v1/databases/{database_id}/query",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    response.raise_for_status()
    data = response.json()
    
    contacts = []
    for page in data.get("results", []):
        props = page["properties"]
        contact = {
            "notion_id": page["id"],
            "name": get_text(props, "Full Name"),
            "phone": get_phone(props, "Phone"),
            "company": get_text(props, "Company"),
            "revenue": get_number(props, "Revenue (RUB)"),
            "profit": get_number(props, "Profit (RUB)"),
            "website": get_url(props, "Website"),
            "rusprofile_url": get_url(props, "RusProfile URL")
        }
        contacts.append(contact)
    
    return contacts

def get_text(props: dict, field: str) -> str:
    """Extract text from Notion field"""
    try:
        if field in props:
            if props[field].get("type") == "title":
                return props[field]["title"][0]["text"]["content"]
            elif props[field].get("type") == "rich_text":
                return props[field]["rich_text"][0]["text"]["content"]
    except (IndexError, KeyError):
        return ""
    return ""

def get_phone(props: dict, field: str) -> str:
    """Extract phone from Notion field"""
    try:
        if field in props and props[field].get("type") == "phone_number":
            return props[field]["phone_number"] or ""
    except (KeyError, TypeError):
        return ""
    return ""

def get_number(props: dict, field: str) -> Optional[int]:
    """Extract number from Notion field"""
    try:
        if field in props and props[field].get("type") == "number":
            return props[field]["number"]
    except (KeyError, TypeError):
        return None
    return None

def get_url(props: dict, field: str) -> Optional[str]:
    """Extract URL from Notion field"""
    try:
        if field in props and props[field].get("type") == "url":
            return props[field]["url"]
    except (KeyError, TypeError):
        return None
    return None
```

### 2. Create Task in SQLite

**After fetching from Notion, create local task:**

```python
def create_task_from_notion_contact(contact: dict, scenario_id: str):
    """Create task in local SQLite"""
    
    task = Task(
        id=uuid.uuid4().hex,
        scenario_id=scenario_id,
        lead_id=contact["notion_id"],
        lead_name=contact["name"],
        lead_phone=contact["phone"],
        lead_company=contact["company"],
        lead_data={
            "revenue": contact["revenue"],
            "profit": contact["profit"],
            "website": contact["website"],
            "rusprofile_url": contact["rusprofile_url"]
        },
        status="pending",
        created_at=datetime.now(),
        retry_count=0,
        max_retries=2
    )
    
    db.session.add(task)
    db.session.commit()
    
    logger.info(f"Created task {task.id} for {contact['name']} ({contact['phone']})")
```

### 3. Update Notion with Results (Sync Back)

**After message sent, update Notion row:**

```python
def update_notion_after_send(
    notion_id: str,
    status: str,  # "sent", "failed", "confirmed"
    message_text: str = None,
    error_message: str = None,
    screenshot_path: str = None
):
    """Update Notion row with execution result"""
    
    # Build update payload
    properties = {
        "Status": {
            "select": {"name": status}
        }
    }
    
    if message_text:
        properties["Last Message"] = {
            "rich_text": [{"text": {"content": message_text[:2000]}}]  # 2000 char limit
        }
    
    if status == "sent":
        properties["Sent via MAX"] = {"checkbox": True}  # Hardcoded for now
        properties["Response Date"] = {
            "date": {"start": datetime.now().date().isoformat()}
        }
    
    if error_message:
        properties["Notes"] = {
            "rich_text": [{"text": {"content": f"Error: {error_message}"}}]
        }
    
    # Request
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28"
    }
    
    response = requests.patch(
        f"https://api.notion.com/v1/pages/{notion_id}",
        headers=headers,
        json={"properties": properties},
        timeout=30
    )
    
    response.raise_for_status()
    logger.info(f"Updated Notion page {notion_id} with status={status}")
```

---

## Polling Schedule & Rate Limiting

### Configuration

```python
# polling_config.py

NOTION_SYNC_CONFIG = {
    "poll_interval_seconds": 60,  # Every 60 seconds
    "page_size": 50,               # Fetch 50 at a time
    "max_retries": 3,              # Retry up to 3 times on failure
    "retry_backoff_seconds": [2, 4, 8],  # Exponential backoff
    "timeout_seconds": 30,         # Per-request timeout
    "max_requests_per_hour": 60,   # Safety limit
}

# Why 60 seconds?
# • 60 requests/hour = 1 request/minute
# • Notion limit: 3 requests/second = 10,800/hour
# • We use: 60/hour = 0.55% of limit
# • Very safe, room for retries and multiple services
```

### Polling Loop

```python
class NotionSyncService:
    def __init__(self, database_id: str, notion_key: str):
        self.database_id = database_id
        self.notion_key = notion_key
        self.last_sync_time = datetime.now() - timedelta(hours=1)  # Start 1 hour ago
        self.sync_count = 0
        
    async def start_polling(self):
        """Main polling loop"""
        while True:
            try:
                await self.sync_contacts()
                self.last_sync_time = datetime.now()
                await asyncio.sleep(60)  # Wait 60 seconds
                
            except requests.Timeout:
                logger.warning("Notion API timeout, retrying in 30 sec")
                await asyncio.sleep(30)
                
            except requests.HTTPError as e:
                if e.response.status_code == 429:  # Rate limit
                    logger.warning("Rate limited by Notion, waiting 60 sec")
                    await asyncio.sleep(60)
                else:
                    logger.error(f"Notion API error: {e}")
                    await asyncio.sleep(30)
                    
            except Exception as e:
                logger.error(f"Unexpected error in polling: {e}")
                await asyncio.sleep(30)
    
    async def sync_contacts(self):
        """Fetch and process new contacts"""
        try:
            contacts = fetch_new_contacts(self.database_id, self.last_sync_time)
            
            if not contacts:
                logger.debug(f"No new contacts at {datetime.now()}")
                return
            
            logger.info(f"Fetched {len(contacts)} new contacts from Notion")
            
            # Create tasks for each contact
            for contact in contacts:
                try:
                    create_task_from_notion_contact(contact, scenario_id="current")
                except Exception as e:
                    logger.error(f"Failed to create task for {contact['name']}: {e}")
                    
            self.sync_count += 1
            
        except requests.Timeout:
            raise  # Re-raise for outer handler
        except Exception as e:
            logger.error(f"Sync error: {e}")
            raise
```

---

## Error Handling & Retry Strategy

### Common Errors

```
401 Unauthorized
  → API key invalid or expired
  → Action: Log error, notify user, stop polling
  
403 Forbidden
  → User not authorized to access this database
  → Action: Log error, notify user, stop polling
  
404 Not Found
  → Database ID wrong
  → Action: Log error, notify user, stop polling
  
429 Too Many Requests
  → Rate limited
  → Action: Wait 60 sec, retry
  
500+ Server Error
  → Notion server issue
  → Action: Wait 30 sec, retry (up to 3 times)
  
Request Timeout (30 sec)
  → Network slow or Notion slow
  → Action: Wait 30 sec, retry (up to 3 times)
```

### Retry Logic

```python
async def fetch_with_retry(
    url: str,
    method: str = "post",
    max_retries: int = 3,
    payload: dict = None
) -> dict:
    """Fetch with exponential backoff"""
    
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28"
    }
    
    for attempt in range(max_retries):
        try:
            if method == "post":
                response = requests.post(url, headers=headers, json=payload, timeout=30)
            elif method == "patch":
                response = requests.patch(url, headers=headers, json=payload, timeout=30)
            else:
                response = requests.get(url, headers=headers, timeout=30)
            
            # Check status
            if response.status_code == 429:  # Rate limit
                wait_time = 60
                logger.warning(f"Rate limited, waiting {wait_time} sec")
                await asyncio.sleep(wait_time)
                continue
            
            if response.status_code >= 500:  # Server error
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # 1, 2, 4 sec
                    logger.warning(f"Server error, retry in {wait_time} sec")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    response.raise_for_status()
            
            # Success
            response.raise_for_status()
            return response.json()
            
        except requests.Timeout:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.warning(f"Timeout, retry in {wait_time} sec")
                await asyncio.sleep(wait_time)
            else:
                raise
                
        except requests.HTTPError as e:
            if e.response.status_code in [401, 403, 404]:
                # Don't retry on auth/not found errors
                raise
            elif attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.warning(f"HTTP error, retry in {wait_time} sec")
                await asyncio.sleep(wait_time)
            else:
                raise
    
    raise Exception("Max retries exceeded")
```

---

## Data Validation

### Phone Number Validation

```python
import re

def validate_phone(phone: str) -> bool:
    """Check if phone is valid format"""
    
    # Normalize: remove spaces, dashes, etc
    normalized = re.sub(r'[^\d+]', '', phone)
    
    # Check: should be 10-15 digits, possibly with +
    if not re.match(r'^\+?[\d]{10,15}$', normalized):
        logger.warning(f"Invalid phone format: {phone}")
        return False
    
    # Check: starts with +7 (Russia) or 7 (without +)
    if not (normalized.startswith('+7') or normalized.startswith('7')):
        logger.warning(f"Phone not Russian: {phone}")
        return False
    
    return True
```

### Company Data Validation

```python
def validate_contact(contact: dict) -> bool:
    """Check if contact has minimum required fields"""
    
    # Required fields
    if not contact.get("name") or not contact.get("name").strip():
        logger.warning("Contact missing name")
        return False
    
    if not contact.get("phone"):
        logger.warning(f"Contact {contact.get('name')} missing phone")
        return False
    
    if not validate_phone(contact["phone"]):
        logger.warning(f"Contact {contact.get('name')} has invalid phone")
        return False
    
    if not contact.get("company") or not contact.get("company").strip():
        logger.warning(f"Contact {contact.get('name')} missing company")
        return False
    
    return True
```

---

## Fallback Strategy (If Notion Down)

### Local Cache

```python
class NotionSyncWithCache:
    def __init__(self):
        self.cache_file = "/data/notion_cache.json"
        self.cache = self.load_cache()
        
    def load_cache(self) -> dict:
        """Load last synced data from disk"""
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_cache(self):
        """Save current state to disk"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)
    
    async def sync_contacts_with_fallback(self):
        """Try Notion, fallback to cache"""
        try:
            # Try to fetch from Notion
            contacts = fetch_new_contacts(self.database_id, self.last_sync_time)
            
            # Save to cache
            self.cache["contacts"] = contacts
            self.cache["last_sync"] = datetime.now().isoformat()
            self.save_cache()
            
            return contacts
            
        except Exception as e:
            logger.error(f"Notion fetch failed: {e}")
            logger.warning("Using cached contacts")
            
            # Use cache
            return self.cache.get("contacts", [])
```

---

## End of 20_NOTION_CRM_SYNC.md

Полная стратегия синхронизации с Notion.

Готов создать **файл 21 (Notion API Details)**?
