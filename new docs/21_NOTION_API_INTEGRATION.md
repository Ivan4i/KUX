# 🔌 NOTION API: Advanced Integration & Optimization

## API Endpoints Reference

### 1. Query Database

**Purpose:** Fetch contacts from Notion database

```
POST https://api.notion.com/v1/databases/{database_id}/query

Headers:
  Authorization: Bearer {NOTION_API_KEY}
  Notion-Version: 2022-06-28
  Content-Type: application/json

Body:
{
  "filter": {...},           // Filter conditions
  "sorts": [...],            // Sort order
  "page_size": 50,           // Results per page
  "start_cursor": "optional" // For pagination
}
```

**Example Query (Get Pending Contacts):**

```json
{
  "filter": {
    "and": [
      {
        "property": "Status",
        "select": {
          "equals": "pending"
        }
      },
      {
        "property": "Phone",
        "rich_text": {
          "is_not_empty": true
        }
      },
      {
        "property": "Created Date",
        "date": {
          "after": "2025-01-20T00:00:00Z"
        }
      }
    ]
  },
  "sorts": [
    {
      "property": "Created Date",
      "direction": "ascending"
    }
  ],
  "page_size": 50
}
```

**Response:**

```json
{
  "object": "list",
  "results": [
    {
      "object": "page",
      "id": "abc123-def456-ghi789",
      "created_time": "2025-01-20T10:15:00.000Z",
      "last_edited_time": "2025-01-27T14:30:00.000Z",
      "properties": {
        "Full Name": {
          "id": "title",
          "type": "title",
          "title": [
            {
              "type": "text",
              "text": {
                "content": "Иван Петров",
                "link": null
              }
            }
          ]
        },
        "Phone": {
          "id": "phone",
          "type": "phone_number",
          "phone_number": "+7-999-123-45-67"
        },
        "Company": {
          "id": "company",
          "type": "rich_text",
          "rich_text": [
            {
              "type": "text",
              "text": {
                "content": "ООО ТДБаза",
                "link": null
              }
            }
          ]
        },
        "Revenue (RUB)": {
          "id": "revenue",
          "type": "number",
          "number": 7000000
        },
        "Status": {
          "id": "status",
          "type": "select",
          "select": {
            "id": "select-1",
            "name": "pending",
            "color": "blue"
          }
        },
        "Sent via MAX": {
          "id": "max-sent",
          "type": "checkbox",
          "checkbox": false
        }
      }
    }
  ],
  "next_cursor": "next-page-cursor-if-exists",
  "has_more": false
}
```

### 2. Update Page (Row)

**Purpose:** Update task status in Notion after message sent

```
PATCH https://api.notion.com/v1/pages/{page_id}

Headers:
  Authorization: Bearer {NOTION_API_KEY}
  Notion-Version: 2022-06-28
  Content-Type: application/json

Body:
{
  "properties": {
    "Status": {
      "select": {"name": "sent"}
    },
    "Last Message": {
      "rich_text": [{"text": {"content": "Message text..."}}]
    },
    "Sent via MAX": {
      "checkbox": true
    },
    "Response Date": {
      "date": {"start": "2025-01-27"}
    }
  }
}
```

**Response:**

```json
{
  "object": "page",
  "id": "abc123-def456-ghi789",
  "created_time": "2025-01-20T10:15:00.000Z",
  "last_edited_time": "2025-01-27T14:45:00.000Z",
  "properties": {
    "Status": {
      "select": {
        "id": "select-2",
        "name": "sent",
        "color": "green"
      }
    }
  }
}
```

### 3. Retrieve Single Page

**Purpose:** Get details of one contact

```
GET https://api.notion.com/v1/pages/{page_id}

Headers:
  Authorization: Bearer {NOTION_API_KEY}
  Notion-Version: 2022-06-28
```

---

## Filter Conditions (Advanced)

### Filter Types

#### Text/Rich Text Fields

```json
// Contains
{
  "property": "Company",
  "rich_text": {
    "contains": "ООО"
  }
}

// Does not contain
{
  "property": "Company",
  "rich_text": {
    "does_not_contain": "Ltd"
  }
}

// Starts with
{
  "property": "Company",
  "rich_text": {
    "starts_with": "ООО"
  }
}

// Is empty
{
  "property": "Company",
  "rich_text": {
    "is_empty": true
  }
}
```

#### Number Fields

```json
// Equals
{
  "property": "Revenue (RUB)",
  "number": {
    "equals": 5000000
  }
}

// Greater than
{
  "property": "Revenue (RUB)",
  "number": {
    "greater_than": 1000000
  }
}

// Less than
{
  "property": "Revenue (RUB)",
  "number": {
    "less_than": 100000000
  }
}

// Between
{
  "property": "Revenue (RUB)",
  "number": {
    "greater_than_or_equal_to": 1000000,
    "less_than_or_equal_to": 100000000
  }
}
```

#### Date Fields

```json
// After
{
  "property": "Created Date",
  "date": {
    "after": "2025-01-20T00:00:00Z"
  }
}

// Before
{
  "property": "Created Date",
  "date": {
    "before": "2025-01-28T00:00:00Z"
  }
}

// This week
{
  "property": "Created Date",
  "date": {
    "this_week": {}
  }
}

// Past month
{
  "property": "Created Date",
  "date": {
    "past_month": {}
  }
}
```

#### Select/Checkbox Fields

```json
// Select equals
{
  "property": "Status",
  "select": {
    "equals": "pending"
  }
}

// Select does not equal
{
  "property": "Status",
  "select": {
    "does_not_equal": "archived"
  }
}

// Checkbox is true
{
  "property": "Sent via MAX",
  "checkbox": {
    "equals": true
  }
}

// Checkbox is false
{
  "property": "Sent via MAX",
  "checkbox": {
    "equals": false
  }
}
```

### Complex Filters (AND/OR Logic)

```json
// Get pending contacts with no phone and revenue > 1M
{
  "filter": {
    "and": [
      {
        "property": "Status",
        "select": {"equals": "pending"}
      },
      {
        "property": "Phone",
        "rich_text": {"is_empty": true}
      },
      {
        "property": "Revenue (RUB)",
        "number": {"greater_than": 1000000}
      }
    ]
  }
}

// Get sent OR confirmed contacts
{
  "filter": {
    "or": [
      {
        "property": "Status",
        "select": {"equals": "sent"}
      },
      {
        "property": "Status",
        "select": {"equals": "confirmed"}
      }
    ]
  }
}

// Complex: (pending AND no_message) OR (sent AND confirmed)
{
  "filter": {
    "or": [
      {
        "and": [
          {
            "property": "Status",
            "select": {"equals": "pending"}
          },
          {
            "property": "Last Message",
            "rich_text": {"is_empty": true}
          }
        ]
      },
      {
        "and": [
          {
            "property": "Status",
            "select": {"equals": "sent"}
          },
          {
            "property": "Response",
            "rich_text": {"is_not_empty": true}
          }
        ]
      }
    ]
  }
}
```

---

## Sorting & Pagination

### Sorts

```json
// Sort by created date (newest first)
{
  "sorts": [
    {
      "property": "Created Date",
      "direction": "descending"
    }
  ]
}

// Multiple sorts (priority + date)
{
  "sorts": [
    {
      "property": "Status",
      "direction": "ascending"
    },
    {
      "property": "Created Date",
      "direction": "ascending"
    }
  ]
}
```

### Pagination

```python
async def fetch_all_contacts(database_id: str) -> List[dict]:
    """Fetch all contacts with automatic pagination"""
    
    all_contacts = []
    cursor = None
    
    while True:
        payload = {
            "page_size": 100,  # Max is 100
        }
        
        if cursor:
            payload["start_cursor"] = cursor
        
        response = await fetch_with_retry(
            f"https://api.notion.com/v1/databases/{database_id}/query",
            "post",
            payload=payload
        )
        
        all_contacts.extend(parse_contacts(response["results"]))
        
        if not response.get("has_more"):
            break
        
        cursor = response.get("next_cursor")
        await asyncio.sleep(0.5)  # Respectful delay between pages
    
    return all_contacts
```

---

## Field Mapping & Type Conversion

### Property Type Reference

| Notion Type | Python Type | Example | Conversion |
|-------------|-------------|---------|------------|
| Title | str | "Иван Петров" | `props["Full Name"]["title"][0]["text"]["content"]` |
| Rich Text | str | "ООО ТДБаза" | `props["Company"]["rich_text"][0]["text"]["content"]` |
| Phone | str | "+7-999-123-45-67" | `props["Phone"]["phone_number"]` |
| Number | int/float | 7000000 | `props["Revenue"]["number"]` |
| Checkbox | bool | true | `props["Sent via MAX"]["checkbox"]` |
| Date | str (ISO) | "2025-01-27" | `props["Response Date"]["date"]["start"]` |
| Select | str | "pending" | `props["Status"]["select"]["name"]` |
| URL | str | "https://..." | `props["Website"]["url"]` |

### Complete Parser

```python
def parse_contact_from_notion(page: dict) -> dict:
    """Convert Notion page to internal contact dict"""
    
    props = page["properties"]
    
    return {
        "notion_id": page["id"],
        "created_at": page["created_time"],
        "updated_at": page["last_edited_time"],
        
        # Text fields
        "name": safe_get_title(props, "Full Name"),
        "company": safe_get_text(props, "Company"),
        "notes": safe_get_text(props, "Notes"),
        "last_message": safe_get_text(props, "Last Message"),
        "response": safe_get_text(props, "Response"),
        
        # Phone
        "phone": safe_get_phone(props, "Phone"),
        
        # URLs
        "website": safe_get_url(props, "Website"),
        "rusprofile_url": safe_get_url(props, "RusProfile URL"),
        
        # Numbers
        "revenue": safe_get_number(props, "Revenue (RUB)"),
        "profit": safe_get_number(props, "Profit (RUB)"),
        
        # Checkboxes
        "sent_via_max": safe_get_checkbox(props, "Sent via MAX"),
        "sent_via_sms": safe_get_checkbox(props, "Sent via SMS"),
        "sent_via_whatsapp": safe_get_checkbox(props, "Sent via WhatsApp"),
        
        # Date
        "response_date": safe_get_date(props, "Response Date"),
        
        # Select
        "status": safe_get_select(props, "Status"),
    }

def safe_get_title(props: dict, field: str) -> str:
    try:
        return props.get(field, {}).get("title", [{}])[0].get("text", {}).get("content", "")
    except (IndexError, KeyError, TypeError):
        return ""

def safe_get_text(props: dict, field: str) -> str:
    try:
        return props.get(field, {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")
    except (IndexError, KeyError, TypeError):
        return ""

def safe_get_phone(props: dict, field: str) -> str:
    try:
        return props.get(field, {}).get("phone_number", "") or ""
    except (KeyError, TypeError):
        return ""

def safe_get_url(props: dict, field: str) -> Optional[str]:
    try:
        url = props.get(field, {}).get("url")
        return url if url else None
    except (KeyError, TypeError):
        return None

def safe_get_number(props: dict, field: str) -> Optional[float]:
    try:
        return props.get(field, {}).get("number")
    except (KeyError, TypeError):
        return None

def safe_get_checkbox(props: dict, field: str) -> bool:
    try:
        return props.get(field, {}).get("checkbox", False)
    except (KeyError, TypeError):
        return False

def safe_get_date(props: dict, field: str) -> Optional[str]:
    try:
        date_obj = props.get(field, {}).get("date")
        if date_obj:
            return date_obj.get("start")
    except (KeyError, TypeError):
        pass
    return None

def safe_get_select(props: dict, field: str) -> Optional[str]:
    try:
        select_obj = props.get(field, {}).get("select")
        if select_obj:
            return select_obj.get("name")
    except (KeyError, TypeError):
        pass
    return None
```

---

## Performance Optimization

### Caching Strategy

```python
class NotionCacheManager:
    """Cache frequently accessed data locally"""
    
    def __init__(self, ttl_seconds: int = 300):  # 5 min cache
        self.cache = {}
        self.ttl_seconds = ttl_seconds
        self.last_fetch = {}
    
    def get_contacts(self, database_id: str) -> Optional[List[dict]]:
        """Get contacts from cache if fresh"""
        
        if database_id not in self.cache:
            return None
        
        age_sec = (time.time() - self.last_fetch[database_id])
        if age_sec > self.ttl_seconds:
            del self.cache[database_id]
            return None
        
        logger.debug(f"Cache hit for {database_id} (age: {age_sec:.1f}s)")
        return self.cache[database_id]
    
    def set_contacts(self, database_id: str, contacts: List[dict]):
        """Save contacts to cache"""
        self.cache[database_id] = contacts
        self.last_fetch[database_id] = time.time()
        logger.debug(f"Cached {len(contacts)} contacts")
    
    def invalidate(self, database_id: str = None):
        """Clear cache"""
        if database_id:
            self.cache.pop(database_id, None)
        else:
            self.cache.clear()
```

### Batch Updates

```python
async def batch_update_status(
    updates: List[Tuple[str, str, str]],  # (notion_id, status, message)
) -> List[bool]:
    """Update multiple rows in Notion"""
    
    results = []
    
    for notion_id, status, message in updates:
        try:
            await update_notion_after_send(notion_id, status, message)
            results.append(True)
            await asyncio.sleep(0.5)  # Rate limiting
        except Exception as e:
            logger.error(f"Failed to update {notion_id}: {e}")
            results.append(False)
    
    return results
```

---

## Notion Auth & Security

### API Key Management

```
# .env file (never commit to git)
NOTION_API_KEY=secret_abc123def456...

# Access in code
from dotenv import load_dotenv
import os

load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")

# In headers
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    ...
}
```

### Token Expiration (Not Applicable)

Notion API keys don't expire. But if compromised:

```
1. Go to https://www.notion.so/my-integrations
2. Find the integration that created the key
3. Regenerate key
4. Update .env
5. Restart backend
```

---

## Rate Limiting & Best Practices

### Rate Limits

```
Notion Public API rate limits:
  • 3 requests per second (per integration)
  • Soft limit: 100 requests per minute recommended
  
Our usage:
  • 1 request per minute (polling)
  • Batch updates: ~10/minute (at peak)
  • Total: ~15 requests/minute = 0.25/sec
  → Well under limits (3/sec)
```

### Best Practices

```
✅ DO:
  • Cache frequently accessed data
  • Batch operations where possible
  • Use filters to reduce data transfer
  • Implement exponential backoff on 429
  • Set page_size = 100 (max) to reduce requests
  
❌ DON'T:
  • Fetch entire database if you only need one row
  • Retry immediately on 429 (rate limit)
  • Update same row more than once per second
  • Leave connections open (use timeout)
  • Log API keys or sensitive data
```

---

## End of 21_NOTION_API_INTEGRATION.md

Полная документация Notion API с примерами.

Готов создать **файл 22 (Notion Webhook Handler)**?
