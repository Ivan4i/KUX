# 🏗️ MASTER CONCEPT PART 2: Complete System Architecture

## Полная Архитектурная Диаграмма

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DESKTOP APP (macOS)                               │
│                       Frontend: React 18 + Vite                            │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Pages/Components (AlignUI only!)                                     │  │
│  │ • Dashboard: 20 Device Cards (realtime status, battery, activity)   │  │
│  │ • Workflow Builder: Visual drag-drop (canvas + properties)          │  │
│  │ • Settings: Rate limits, warmup config, channel priority            │  │
│  │ • Logs: SQLite + Telegram logs viewer                              │  │
│  │ • Device Manager: List all devices, health status                  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│  Styling: AlignUI components, theme.ts tokens, anime.js animations       │
│  State: Zustand (global state)                                            │
│  API: Axios service layer (no direct fetch calls)                        │
└──────────────────────────────────────────────────────────────────────────┘
         │
         │ HTTP/WebSocket (localhost:8000)
         │
         ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BACKEND API SERVER                                  │
│                   Python 3.11 + FastAPI + asyncio                          │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │ API Routes (RESTful + WebSocket)                                   │   │
│  │ • GET  /api/scenarios (list all)                                  │   │
│  │ • POST /api/scenarios (create new)                                │   │
│  │ • GET  /api/scenarios/{id} (fetch one)                           │   │
│  │ • POST /api/scenarios/{id}/run (trigger execution)               │   │
│  │ • GET  /api/devices (list 20 devices + status)                   │   │
│  │ • GET  /api/tasks (list pending/running/completed)               │   │
│  │ • GET  /api/logs (fetch execution logs)                          │   │
│  │ • WS   /ws/execution/{task_id} (realtime progress)               │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │ Core Services Layer                                                │   │
│  │                                                                    │   │
│  │ ScenarioService:                                                 │   │
│  │  • CRUD operations on scenarios                                  │   │
│  │  • Workflow DAG validation (topological sort)                    │   │
│  │  • Schedule execution (add to queue)                             │   │
│  │                                                                    │   │
│  │ ExecutionEngine:                                                 │   │
│  │  • Main orchestrator (runs scenarios step by step)               │   │
│  │  • Handles workflow DAG execution                                │   │
│  │  • Error recovery (retry, fallback channels)                     │   │
│  │  • WebSocket fanout (send progress to all frontend clients)      │   │
│  │  • Logging (every step → SQLite + Telegram)                      │   │
│  │                                                                    │   │
│  │ DevicePoolManager:                                               │   │
│  │  • Allocate devices (pick least busy device)                     │   │
│  │  • Health monitoring (ADB ping every 30 sec)                     │   │
│  │  • Max concurrent: 3 executions at once                          │   │
│  │  • Queue other tasks (FIFO)                                      │   │
│  │  • Device reconnect (if offline)                                 │   │
│  │                                                                    │   │
│  │ NotionSync:                                                      │   │
│  │  • Polling 1/min to Notion API                                   │   │
│  │  • Fetch rows with status='pending'                              │   │
│  │  • Idempotency (don't run same task twice)                       │   │
│  │  • Update status back (pending → processing → sent → confirmed)  │   │
│  │  • Update checklist (sent_via_max ✓, sent_via_sms ✓, etc)      │   │
│  │  • Retry on timeout/rate limit                                   │   │
│  │                                                                    │   │
│  │ GeminiService:                                                   │   │
│  │  • Upload 20 .md context files (once, cached in Gemini)         │   │
│  │  • Build prompt: {rusprofile_url, website, director, revenue}   │   │
│  │  • Call Gemini 3 Pro API (with caching)                          │   │
│  │  • Parse response: {message, confidence, flags}                  │   │
│  │  • Timeout handling (30 sec max)                                 │   │
│  │  • Fallback to template (if Gemini fails)                        │   │
│  │                                                                    │   │
│  │ TelegramLogger:                                                  │   │
│  │  • Send batch logs to Telegram chat                              │   │
│  │  • Format: "✓ Lead Name → SMS sent at 22:30"                    │   │
│  │  • Or: "✗ Lead Name → WhatsApp error: contact_not_found"        │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │ Agent Layer (Executes on Android Devices)                        │   │
│  │                                                                    │   │
│  │ BaseAgent (abstract):                                            │   │
│  │  • initialize(device_id)                                         │   │
│  │  • execute_step(step) → steps are: open_app, find_contact, etc   │   │
│  │  • validate_result(expected_result)                              │   │
│  │  • cleanup()                                                     │   │
│  │  • Includes HumanBehavior injection at every step                │   │
│  │                                                                    │   │
│  │ MAXAgent(BaseAgent):                                             │   │
│  │  • Specific UIAutomator paths for MAX app                        │   │
│  │  • Steps: open MAX → find contact → type message → send          │   │
│  │  • Fallback to Gemini Vision if UI changed                       │   │
│  │                                                                    │   │
│  │ SMSAgent(BaseAgent):                                             │   │
│  │  • Native Android SMS API (not UIAutomator)                      │   │
│  │  • Steps: build SMS → send via SmsManager → check delivery       │   │
│  │                                                                    │   │
│  │ WhatsAppAgent(BaseAgent):                                        │   │
│  │  • UIAutomator paths for WhatsApp app                            │   │
│  │  • Steps: open WhatsApp → find contact → type → send             │   │
│  │  • Fallback to Gemini Vision if UI changed                       │   │
│  │                                                                    │   │
│  │ Each agent includes HumanBehavior:                               │   │
│  │  • HumanTyping (per-char delays, backspace, pauses)              │   │
│  │  • HumanTiming (random pause between actions 2-7 sec)            │   │
│  │  • HumanGestures (scroll, tap with natural speed)                │   │
│  │  • Warmup scenarios (prewarm before sending)                     │   │
│  │  • Anti-detection patterns (avoid bot detection)                 │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │ Queue & Scheduler                                                 │   │
│  │                                                                    │   │
│  │ AsyncIO Queue:                                                   │   │
│  │  • FIFO task queue                                               │   │
│  │  • Max 3 concurrent workers (rest in queue)                      │   │
│  │  • Backpressure handling (reject if overflow)                    │   │
│  │  • Graceful shutdown (finish current, reject new)                │   │
│  │                                                                    │   │
│  │ Scheduler:                                                       │   │
│  │  • Cron-like scheduling (can set time when to run)               │   │
│  │  • Manual trigger (Run button in Dashboard)                      │   │
│  │  • Retry scheduling (if failed, retry in 5 min)                  │   │
│  │  • Pause/Resume (can pause campaign mid-execution)               │   │
│  │  • Kill-switch (STOP button, emergency stop all)                 │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │ Data Layer                                                         │   │
│  │                                                                    │   │
│  │ SQLite Database (local, Mac):                                    │   │
│  │  • scenarios (id, name, description, steps, status)              │   │
│  │  • devices (id, name, status, battery, last_activity)            │   │
│  │  • tasks (id, scenario_id, status, created_at, updated_at)       │   │
│  │  • executions (id, task_id, device_id, step_idx, result, error)  │   │
│  │  • logs (id, task_id, level, message, timestamp)                 │   │
│  │                                                                    │   │
│  │ Redis Cache (optional, for queue state):                         │   │
│  │  • Task queue (if distributed later)                             │   │
│  │  • Session cache                                                 │   │
│  │  • Rate limit counters (per device/hour)                         │   │
│  └────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  Logging: Loguru (structured logs to console + file)                       │
│  Config: Environment variables (.env file)                                 │
└─────────────────────────────────────────────────────────────────────────────┘
         │
         │ ADB USB Protocol (localhost:5037)
         │
         ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                     ANDROID DEVICE FLEET (20 devices)                       │
│                  Google Pixel 5 (locally connected via USB hub)             │
│                                                                              │
│  Device 1: ┌──────────────────────────────────────────────────────────┐   │
│  ├─ ADB Daemon (listens on USB)                                      │   │
│  ├─ UIAutomator2 Service (handles UI automation)                     │   │
│  ├─ Applications:                                                    │   │
│  │  ├─ MAX app (messaging)                                          │   │
│  │  ├─ SMS app (native messaging)                                   │   │
│  │  ├─ WhatsApp                                                     │   │
│  │  └─ Chrome (for Scrcpy stream)                                   │   │
│  ├─ Scrcpy server (screen mirroring for manual override)           │   │
│  └─ SIM card (with corporate SMS plan)                             │   │
│                                                                      │   │
│  Device 2-20: [Same structure]                                      │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  All devices connected to Mac via:                                         │
│  • ORICO USB Hub (10 ports, expandable)                                    │
│  • USB 3.0 cables                                                         │
│  • ADB over USB (persistent connection with auto-reconnect)               │
└─────────────────────────────────────────────────────────────────────────────┘
         │
         │ Network (HTTP API)
         │
         ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                       EXTERNAL SERVICES                                     │
│                                                                              │
│  Notion API:                                                                │
│  • CRM database (leads with status, channels, metadata)                    │
│  • Polling 1/min → fetch pending rows                                      │
│  • Update statuses back (sent, failed, confirmed)                          │
│  • Idempotent operations                                                   │
│                                                                              │
│  Gemini 3 Pro API:                                                         │
│  • 20 .md context files (business analysis, writing rules, examples)       │
│  • Per-lead analysis: rusprofile → personalized message                    │
│  • Response: message + confidence + flags                                  │
│  • Caching enabled (save tokens and time)                                  │
│                                                                              │
│  Telegram Bot API:                                                          │
│  • Send batch logs (every execution completes)                             │
│  • Format: "✓ Lead Name → Channel sent at time"                            │
│  • Real-time notifications for critical errors                             │
│                                                                              │
│  RusProfile API (optional):                                                │
│  • Scrape company data (if website not available)                          │
│  • Revenue, profit, director name                                          │
│  • Used as fallback if Notion data incomplete                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow (Пошаговый E2E Example)

**Пример:** Кампания с 3 лидами, device pool из 2 устройств

### Step 1: User Trigger (t=0:00)

```
Dashboard: User clicks "Run Campaign"
  → Frontend POST /api/scenarios/campaign-1/run
  → Backend adds to queue: Task(id=task-001, scenario_id=campaign-1, status=pending)
  → WebSocket broadcast: {"status": "campaign_started", "total_leads": 3}
```

### Step 2: Notion Fetch (t=0:01)

```
NotionSync service (runs every 1 minute):
  → GET Notion: SELECT * WHERE status='pending' LIMIT 3
  → Returns:
    - Lead 1: Иван Петров, ООО "ТДБаза", выручка 7млн, +7-999-123-45-67
    - Lead 2: Александр Сидоров, ФГБУ, выручка 321млн, +7-888-234-56-78
    - Lead 3: Мария Шарова, ИП, выручка 2млн, +7-777-345-67-89
  → Update in Notion: status='processing' for all 3
```

### Step 3: Gemini Analysis (t=0:02 - 0:05)

```
For each lead:
  GeminiService:
    1. Upload 20 .md context (once, cached): {business_analysis, sales_rules, examples, ...}
    2. Build prompt: {rusprofile_url: "https://rusprofile.ru/id/...", 
                       website: "...", 
                       director_name: "Иван Петров", 
                       revenue: 7000000, 
                       profit: 500000}
    3. Call Gemini 3 Pro (with cache prefix)
    4. Response: {
         message: "Иван, видел что у вас выручка 7млн...",
         confidence: 95,
         flags: []
       }
    5. If confidence < 50 or "insufficient_data" → fallback template

  Result: 3 personalized messages ready
```

### Step 4: Device Allocation (t=0:06)

```
DevicePoolManager:
  • Devices available: 20 total
  • Current load: device-01 (busy), device-02 (idle), device-03 (idle), ...
  • Allocate task 1 → device-02 (least busy)
  • Allocate task 2 → device-03 (least busy, after device-02)
  • Queue task 3 (max concurrent = 3, but we have capacity for all 3)
  • Actually allocate task 3 → device-04

  Execution starts on 3 devices in parallel
```

### Step 5: Execution on Device (Example: device-02, lead 1)

```
MAXAgent(device_id="device-02", message="Иван, видел что у вас выручка 7млн..."):

[Step 1] Initialize HumanBehavior context
  • Warmup: already done on device-02
  • Rate limit check: 3/10 messages today (OK)

[Step 2] Open MAX app
  • ADB shell: "am start -n com.alibaba.mobileim/.MainActivity"
  • HumanTiming pause: 1200ms (random 800-1600)
  • Wait for app to load: 2000ms
  • Take screenshot

[Step 3] Find contact (+7-999-123-45-67)
  • UIAutomator: find element with resource_id="com.alibaba.mobileim:id/search"
  • HumanTiming pause: 300ms (before click)
  • Click search box
  • HumanTiming pause: 400ms (after click)
  
  [Step 3a] Type phone number with HumanBehavior:
    • "+" → wait 80ms
    • "7" → wait 95ms (faster digit)
    • "-" → PAUSE 200ms (symbol, human thinks a bit)
    • "9" → wait 85ms
    • "9" → wait ERROR! typed "8" instead, wait 150ms (human notices)
    • Backspace → wait 100ms (delete)
    • "9" → wait 85ms (corrected)
    • [continue typing rest of number...]
    • Total typing time: ~2500ms (realistic for 15-char phone)
  
  • HumanTiming pause: 400ms (after typing)
  • ADB shell: press ENTER or click search
  • Wait for search results: 1500ms
  • Take screenshot

[Step 4] Tap on found contact
  • UIAutomator finds contact in results
  • HumanTiming pause: 350ms (before click)
  • Tap contact
  • HumanTiming pause: 500ms (app opens chat, human reads)
  • Wait for chat to load: 1000ms

[Step 5] Type message with HumanBehavior (CRITICAL!):
  • Message: "Иван, видел что у вас выручка 7млн..." (200 chars)
  
  Typing flow:
    • Click message input field
    • HumanTiming pause: 400ms (before start typing, human gathers thoughts)
    • Start typing:
      • Char 1-10: 2 chars/sec (fast start)
      • Char 11-20: 1.5 chars/sec (slows down, thinking)
      • Char 21-25: type wrong word → Backspace 5x → retype (mistake!)
      • Char 26-50: 1.8 chars/sec (corrected, moving on)
      • [PAUSE 300ms before comma] (punctuation pause)
      • Continue until end
    
    • Total typing time: ~45-60 seconds (REALISTIC for 200-char message!)
    • Total message: original 200 chars + mistakes + corrections = ~260 actual keystrokes
  
  • After typing: take screenshot
  • HumanTiming pause: 500ms (proofread before sending)

[Step 6] Send message
  • HumanTiming pause: 200ms (before final click)
  • Tap "Send" button
  • HumanTiming pause: 1000ms (wait to see delivery)
  • Wait for "✓ Delivered" or "✓✓ Read"

[Step 7] Validate
  • Take final screenshot
  • Check if message visible in chat
  • Look for delivery checkmarks
  • If success: return {status: "sent", screenshot: "..."}
  • If error (contact not found, app crashed, etc): return {status: "failed", error: "..."}

[Step 8] Cleanup & Report
  • Close MAX app (back home)
  • Log result to SQLite
  • Send to Telegram: "✓ Иван Петров → MAX sent at 22:45"
  • Update Notion: status='sent', sent_via_max=✓, timestamp
  • WebSocket broadcast to Dashboard: Task progress update
```

**Execution time for this device:**
- Warmup: N/A (already done)
- Open app: 2.2 sec
- Find contact: 2.5 sec + search wait
- Type message: 50-60 sec
- Send + validate: 2 sec
- **Total: ~60-70 seconds** (matches human speed!)

### Step 6: Parallel Execution

```
At same time (t=0:06 to t=1:15):
  • device-02: Lead 1 (MAXAgent) → 60-70 sec
  • device-03: Lead 2 (WhatsAppAgent) → 60-70 sec
  • device-04: Lead 3 (SMSAgent) → 15-20 sec

At t=1:15 all complete. Results collected.
```

### Step 7: Status Sync Back to Notion (t=1:20)

```
NotionSync (next polling cycle):
  → GET all tasks with status='completed'
  → For each completed task:
    • Update Notion row: status='sent', sent_via_channel=✓, timestamp
    • If failed: status='failed', error_message
  → Notion updated for all 3 leads
```

### Step 8: Telegram Notification (t=1:21)

```
TelegramLogger:
  → Send batch message:
    ✓ Иван Петров (ООО "ТДБаза") → MAX отправлено в 22:45
    ✓ Александр Сидоров (ФГБУ) → WhatsApp отправлено в 22:46
    ✓ Мария Шарова (ИП) → SMS отправлено в 22:47
    
    Summary: 3/3 успешно за 80 сек
```

### Step 9: Dashboard Update (realtime via WebSocket)

```
WebSocket stream (every step):
  • device-02: "typing message..." (50-60 sec progress bar)
  • device-03: "waiting for delivery..." 
  • device-04: "completed"
  
Final state:
  • device-02: idle (last activity: Lead 1 sent)
  • device-03: idle (last activity: Lead 2 sent)
  • device-04: idle (last activity: Lead 3 sent)
  • Total: 3 messages sent, 0 failed
```

---

## Component Interactions (Таблица Взаимодействий)

| Component | Calls | Purpose |
|-----------|-------|---------|
| Frontend (Dashboard) | → Backend (HTTP) | Fetch devices, tasks, logs |
| Frontend | ← Backend (WebSocket) | Realtime progress updates |
| Backend API Routes | → ScenarioService | CRUD scenarios |
| Backend API Routes | → ExecutionEngine | Trigger scenario run |
| ExecutionEngine | → DevicePoolManager | Pick device for execution |
| ExecutionEngine | → NotionSync | Fetch pending tasks |
| ExecutionEngine | → GeminiService | Analyze lead, generate message |
| ExecutionEngine | → Agents (MAXAgent, etc) | Execute on device |
| ExecutionEngine | → TelegramLogger | Send logs |
| ExecutionEngine | → SQLite | Write logs + task results |
| DevicePoolManager | ← ADB | Get device status, reconnect |
| Agents (MAXAgent) | ← ADB | UIAutomator commands |
| Agents (SMSAgent) | ← ADB | Android SMS API |
| GeminiService | → Gemini API | Analyze leads |
| NotionSync | ← Notion API | Fetch/update tasks |
| NotionSync | → Notion API | Update status back |
| TelegramLogger | → Telegram API | Send notifications |

---

## Security Boundaries

```
┌─ Public Internet
│   • Notion API (controlled, IP whitelist possible)
│   • Gemini 3 Pro API (Google service, HTTPS)
│   • Telegram Bot API (controlled, token protected)
│   • RusProfile (read-only scraping)
│
├─ Private Network (Mac)
│   • Backend FastAPI (localhost:8000, local only)
│   • SQLite database (local file, encrypted optional)
│   • Frontend React (localhost:3000, local only)
│
└─ Local USB Bus
    • ADB connections (USB-only, no network exposure)
    • Scrcpy (local socket, no remote access needed)
    • Android devices (never exposed to internet)
```

**Secrets Management:**
- API keys in `.env` file (never in code)
- `.env` in .gitignore
- Notion API key (read-only or specific database)
- Gemini API key (quota limits set)
- Telegram bot token (specific chat only)

---

## Concurrency & Performance

**Thread Model:**
- Backend: FastAPI with async/await (Python asyncio)
- Frontend: React with async state updates
- Device execution: Sequential per device (one task at a time per device)
- Max concurrent: 3 devices executing in parallel
- Queue: FIFO, backpressure if overflow

**Performance Targets:**
- Message sending: 60-70 sec per message (includes HumanBehavior)
- Throughput: ~3 concurrent × 60 sec = 3 messages/min = 180 messages/hour
- Daily capacity: 20 devices × 30 messages/day = 600 messages/day (if running all day)
- Actual sustainable: 200-300 messages/day (respecting rate limits + safety margins)

**Bottlenecks (in order of impact):**
1. Device execution time (60 sec per message) — can't speed up without breaking HumanBehavior
2. Notion API polling (1/min) — acceptable, trade-off for simplicity
3. Gemini API latency (2-5 sec per request) — mitigated by caching
4. USB bandwidth (not a bottleneck at USB 3.0 speeds)

---

## End of Part 2

**Part 3:** Критические уязвимости и решения для каждой проблемы

---

**Архитектура готова. Part 2 содержит:**
- ✅ Полная диаграмма всех компонентов
- ✅ Все слои системы (frontend, backend, agents, devices)
- ✅ E2E data flow с реальным примером (3 лида, 2 устройства)
- ✅ Таблица взаимодействий компонентов
- ✅ Границы безопасности
- ✅ Модель конкурентности и производительность

Готов создать **Part 3 (Уязвимости & Решения)** с самых важных проблем?
