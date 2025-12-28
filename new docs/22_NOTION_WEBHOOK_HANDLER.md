# 🪝 NOTION WEBHOOKS: Event-Driven Sync (Future Enhancement)

## Overview

**Current Implementation:** Polling-based (every 60 seconds)
**Future Enhancement:** Webhook-based (real-time updates)

Note: Notion webhooks are limited (beta), so polling is primary. Webhooks are documented here for future upgrade.

---

## Webhook Architecture (When Available)

### Setup Process

```
1. Notion Dashboard:
   Settings → Integrations → My integrations
   → Find "Automation Sync"
   → Advanced → Webhooks
   
2. Create Webhook:
   URL: https://your-server.local:8000/webhooks/notion
   Events: page updated, page deleted
   Subscriptions: database changes
   
3. Backend receives:
   POST /webhooks/notion
   Headers: X-Notion-Signature (for verification)
   Body: {event_type, database_id, page_id, changes}
```

### Webhook Payload Example

```json
{
  "event_type": "page.updated",
  "database_id": "abc123def456",
  "page": {
    "id": "page-id-123",
    "properties": {
      "Status": {
        "select": {"name": "sent"}
      }
    }
  },
  "timestamp": "2025-01-27T14:30:00.000Z",
  "signature": "sha256=abcdef123456..."
}
```

### Webhook Handler (FastAPI)

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import hashlib
import hmac

app = FastAPI()

# Notion webhook secret (from dashboard)
NOTION_WEBHOOK_SECRET = os.getenv("NOTION_WEBHOOK_SECRET")

@app.post("/webhooks/notion")
async def handle_notion_webhook(request: Request):
    """Handle real-time updates from Notion"""
    
    # Get signature
    signature = request.headers.get("X-Notion-Signature")
    body = await request.body()
    
    # Verify signature
    expected_signature = hmac.new(
        NOTION_WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Parse payload
    payload = await request.json()
    
    # Handle event
    event_type = payload.get("event_type")
    
    if event_type == "page.updated":
        await handle_page_updated(payload)
    elif event_type == "page.deleted":
        await handle_page_deleted(payload)
    else:
        logger.warning(f"Unknown event type: {event_type}")
    
    return JSONResponse({"status": "ok"}, status_code=200)

async def handle_page_updated(payload: dict):
    """Handle page update event"""
    
    page_id = payload["page"]["id"]
    changes = payload.get("changes", {})
    
    logger.info(f"Notion page updated: {page_id}")
    
    # Parse changes
    if "Status" in changes:
        new_status = changes["Status"]["select"]["name"]
        logger.info(f"Status changed to: {new_status}")
        
        # Invalidate cache, re-fetch from DB
        notion_cache.invalidate()
        
        # Update local database if needed
        if new_status in ["sent", "confirmed"]:
            task = db.session.query(Task).filter_by(lead_id=page_id).first()
            if task:
                task.status = new_status
                task.notion_updated = True
                db.session.commit()

async def handle_page_deleted(payload: dict):
    """Handle page deletion"""
    
    page_id = payload["page"]["id"]
    logger.warning(f"Notion page deleted: {page_id}")
    
    # Mark task as archived locally
    task = db.session.query(Task).filter_by(lead_id=page_id).first()
    if task:
        task.status = "archived"
        db.session.commit()
```

### Why Webhooks (Currently Problematic)

```
✅ Advantages:
  • Real-time updates (no 60 sec delay)
  • No wasted API calls (only on actual changes)
  • Lower API quota usage
  
❌ Current Issues:
  • Notion webhooks are in beta (unstable)
  • Limited event types (not all changes trigger)
  • Requires public URL (can't use localhost)
  • Complex signature verification
  • Notion frequently changes webhook API
  
✅ Solution for Now:
  • Stick with polling (reliable, proven)
  • Implement webhook handler as optional backup
  • Enable webhooks once Notion stabilizes
```

---

## Polling vs Webhooks Comparison

| Aspect | Polling | Webhooks |
|--------|---------|----------|
| **Real-time** | 60 sec delay | Instant |
| **API Calls** | 1/minute always | Only on changes |
| **Reliability** | ✅ Stable | ⚠️ Beta |
| **Complexity** | Low | High (signatures) |
| **Cost** | Lower | Lower (fewer calls) |
| **Offline Tolerance** | ✅ Catches up | ❌ Misses events |
| **Debugging** | Easy logs | Hard to reproduce |
| **Fallback** | N/A | Polling as fallback |

**Recommendation:** Polling primary + Webhooks as opt-in feature

---

## Hybrid Approach (Polling + Optional Webhooks)

### Config

```python
# config.py
SYNC_MODE = "polling"  # or "hybrid"

POLLING_CONFIG = {
    "enabled": True,
    "interval_seconds": 60,
    "timeout_seconds": 30,
}

WEBHOOK_CONFIG = {
    "enabled": False,  # Set to True if Notion webhooks stable
    "verify_signature": True,
    "timeout_seconds": 10,
}
```

### Fallback Logic

```python
class NotionSyncHybrid:
    def __init__(self):
        self.last_sync = None
        self.use_webhooks = WEBHOOK_CONFIG["enabled"]
        
    async def sync_contacts(self):
        """Use webhooks if available, fallback to polling"""
        
        if self.use_webhooks:
            logger.info("Waiting for webhook events...")
            # Webhook handler will call update methods
            # But also run polling as safety net
            await asyncio.sleep(60)
            # Fallback poll
            await self.poll_contacts()
        else:
            # Polling only
            await self.poll_contacts()
    
    async def poll_contacts(self):
        """Fallback polling"""
        logger.debug("Polling Notion for changes...")
        contacts = fetch_new_contacts(...)
        # Process contacts
```

---

## Error Handling in Webhooks

### Webhook Failure Scenarios

```python
async def handle_notion_webhook(request: Request):
    try:
        # Signature check
        if not verify_signature(request):
            raise HTTPException(status_code=401)
        
        payload = await request.json()
        
        # Process event
        try:
            await process_webhook_event(payload)
            return {"status": "ok"}
        except Exception as e:
            logger.error(f"Webhook processing failed: {e}")
            # Return 200 anyway (Notion will retry if we return error)
            # But log for manual review
            return {"status": "error", "message": str(e)}
            
    except Exception as e:
        logger.error(f"Webhook handler error: {e}")
        # Always return 200 to prevent Notion from retrying
        # (we'll catch up via polling)
        return {"status": "error"}
```

### Webhook Retry Strategy

```
Notion retries webhooks:
  • Attempt 1: Immediate
  • Attempt 2: 30 seconds later
  • Attempt 3: 2 minutes later
  • Attempt 4: 10 minutes later
  • Max retries: 3 times

If all fail:
  • Notion disables webhook
  • We get email notification
  • We can re-enable in dashboard
  • Polling catches up on next cycle
```

---

## Monitoring Webhooks

### Webhook Health Check

```python
@app.get("/health/webhooks")
async def webhook_health():
    """Check webhook status"""
    
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28"
    }
    
    response = requests.get(
        "https://api.notion.com/v1/webhooks",  # Hypothetical endpoint
        headers=headers
    )
    
    webhooks = response.json()
    
    return {
        "webhook_count": len(webhooks),
        "active": sum(1 for w in webhooks if w["status"] == "active"),
        "failed": sum(1 for w in webhooks if w["status"] == "failed"),
        "last_event": webhooks[0]["last_event_time"] if webhooks else None
    }
```

---

## End of 22_NOTION_WEBHOOK_HANDLER.md

Документация для future webhook enhancement (сейчас не используется).

Теперь создаю **файл 23 (Error Handling)**:
