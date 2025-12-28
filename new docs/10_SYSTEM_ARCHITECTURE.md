# 🏗️ СИСТЕМА АРХИТЕКТУРА: Полная Диаграмма

## Многоуровневая Архитектура (5 слоёв)

```
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 1: PRESENTATION (Frontend)                               │
│ React 18 + Vite + AlignUI Components + Zustand                │
│ • Dashboard (realtime device cards)                            │
│ • Workflow Builder (visual drag-drop)                          │
│ • Device Manager (health monitoring)                           │
│ • Logs Viewer (SQLite + Telegram)                              │
│ • Settings (rate limits, paths, config)                        │
│ localhost:3000 (development) / localhost:3000 (production)    │
└─────────────────────────────────────────────────────────────────┘
                            ↕ (HTTP/WebSocket)
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 2: API GATEWAY & ORCHESTRATION (Backend)                │
│ FastAPI + Python 3.11 + asyncio                                │
│ • REST API routes (/api/scenarios, /api/devices, etc)         │
│ • WebSocket endpoints (realtime progress)                      │
│ • Request validation & error handling                          │
│ • Authentication (local user only)                             │
│ • Rate limiting & backpressure                                 │
│ localhost:8000 (local only)                                    │
└─────────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 3: BUSINESS LOGIC (Services)                             │
│                                                                 │
│ ScenarioService:                                               │
│  • CRUD scenarios                                              │
│  • Workflow DAG validation (topological sort)                  │
│  • Trigger execution → add to queue                            │
│                                                                 │
│ ExecutionEngine (Main Orchestrator):                           │
│  • Runs scenarios step-by-step                                 │
│  • Handles workflow DAG execution                              │
│  • Error recovery & retry logic                                │
│  • WebSocket fanout (progress updates)                         │
│  • Logging (SQLite + Telegram)                                 │
│  • Kill-switch handling (pause/resume/stop)                    │
│                                                                 │
│ DevicePoolManager:                                             │
│  • Allocate devices (pick least busy)                          │
│  • Health monitoring (ADB ping every 30 sec)                   │
│  • Max concurrent: 3 executions                                │
│  • Queue management (FIFO)                                     │
│  • Device reconnect logic                                      │
│  • Rate limit enforcement (per device/hour)                    │
│                                                                 │
│ NotionSync:                                                    │
│  • Polling 1/min to Notion API                                 │
│  • Fetch rows with status='pending'                            │
│  • Idempotency checking (no duplicate runs)                    │
│  • Update status back (pending → sent → confirmed)            │
│  • Update checklists (sent_via_max ✓, etc)                    │
│  • Exponential backoff on rate limit                           │
│                                                                 │
│ GeminiService:                                                 │
│  • Upload 20 .md context (cached in Gemini)                   │
│  • Build prompt from lead data                                 │
│  • Call Gemini 3 Pro API                                       │
│  • Parse response + confidence scoring                         │
│  • Fallback template on fail                                   │
│  • Timeout handling (30 sec max)                               │
│                                                                 │
│ TelegramLogger:                                                │
│  • Batch send logs to Telegram chat                            │
│  • Format: "✓ Lead → Channel sent"                             │
│  • Critical alerts (device offline, captcha)                   │
│  • Daily summary                                               │
│                                                                 │
│ ScreenshotService:                                             │
│  • Save screenshots after send                                 │
│  • Organize by date/task_id                                    │
│  • Serve via HTTP endpoint                                     │
│  • Cleanup old screenshots (7-day retention)                   │
└─────────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 4: AGENTS & EXECUTION (Android Automation)              │
│                                                                 │
│ BaseAgent (abstract):                                          │
│  • initialize(device_id) → connect via ADB                     │
│  • execute_step(step) → run one step                           │
│  • validate_result(expected) → check success                   │
│  • cleanup() → close apps                                      │
│  • INCLUDES: HumanBehavior injection at every step             │
│                                                                 │
│ MAXAgent(BaseAgent):                                           │
│  • MAX app automation (UIAutomator)                            │
│  • Steps: open → find contact → type → send                    │
│  • Fallback to Gemini Vision if UI changed                     │
│  • Screenshot validation                                       │
│                                                                 │
│ SMSAgent(BaseAgent):                                           │
│  • Native Android SMS API (not UIAutomator)                    │
│  • Steps: build SMS → send via SmsManager                      │
│  • Delivery verification                                       │
│                                                                 │
│ WhatsAppAgent(BaseAgent):                                      │
│  • WhatsApp UIAutomator automation                             │
│  • Steps: open → find contact → type → send                    │
│  • Fallback to Gemini Vision                                   │
│                                                                 │
│ HumanBehavior (Injected in All Agents):                        │
│  • HumanTyping: per-char delays, backspace, pauses             │
│  • HumanTiming: random delays between actions                  │
│  • HumanGestures: scroll, swipe, tap (natural speed)           │
│  • WarmupScenario: prewarm before sending                      │
│  • AntiDetectionPatterns: avoid bot detection                  │
└─────────────────────────────────────────────────────────────────┘
                            ↕ (ADB USB Protocol)
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 5: HARDWARE (Android Devices)                            │
│                                                                 │
│ 20 × Google Pixel 5 devices:                                   │
│  • Connected via ORICO USB Hub (USB 3.0)                       │
│  • ADB daemon on each device                                   │
│  • UIAutomator2 service                                        │
│  • Apps: MAX, SMS, WhatsApp                                    │
│  • Scrcpy server (for manual override)                         │
│  • Each has corporate SIM card                                 │
│                                                                 │
│ All devices:                                                   │
│  • LOCAL to Mac (no network exposure)                          │
│  • TCP ADB mode enabled                                        │
│  • Auto-reconnect on disconnect                                │
│  • Health monitoring every 30 sec                              │
└─────────────────────────────────────────────────────────────────┘
                            ↕ (HTTP API)
┌─────────────────────────────────────────────────────────────────┐
│ EXTERNAL INTEGRATIONS                                          │
│                                                                 │
│ Notion API (CRM database):                                     │
│  • Fetch leads (status='pending')                              │
│  • Update status + checklists                                  │
│                                                                 │
│ Gemini 3 Pro API:                                              │
│  • Analyze leads + generate messages                           │
│  • Vision fallback for UI recognition                          │
│                                                                 │
│ Telegram Bot API:                                              │
│  • Send batch logs + alerts                                    │
│  • Real-time notifications                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Communication Matrix

### Synchronous Calls (Request-Response)

| Caller | Called | Method | Purpose | Timeout |
|--------|--------|--------|---------|---------|
| Frontend | Backend API | HTTP GET/POST | Fetch/trigger | 10 sec |
| Backend API | ScenarioService | Python call | CRUD scenarios | N/A |
| ExecutionEngine | DevicePoolManager | Python call | Allocate device | N/A |
| ExecutionEngine | GeminiService | HTTP API call | Analyze lead | 30 sec |
| DevicePoolManager | ADB | Shell command | Health check | 5 sec |
| MAXAgent | ADB | UIAutomator | Find element | 10 sec |
| MAXAgent | Gemini Vision | HTTP API | Fallback UI | 5 sec |

### Asynchronous Events (Fire-and-Forget)

| Emitter | Listener | Event | Latency |
|---------|----------|-------|---------|
| ExecutionEngine | Frontend (WebSocket) | Progress update | 0 sec (realtime) |
| ExecutionEngine | SQLite | Log write | <1 sec |
| ExecutionEngine | TelegramLogger | Send logs | <5 sec |
| ExecutionEngine | NotionSync | Update status | 1-10 sec |
| DevicePoolManager | Frontend (WebSocket) | Device status | 30 sec |

---

## Data Flow: Request Through All Layers

```
USER ACTION: Clicks "Run Campaign" in Dashboard

LAYER 1 (Frontend):
  • React component: onClick → dispatch Zustand action
  • Zustand: apiService.runCampaign(scenario_id)
  • Axios: POST /api/scenarios/{id}/run
  ↓

LAYER 2 (API Gateway):
  • FastAPI route: @app.post("/api/scenarios/{id}/run")
  • Validation: scenario exists, status is "pending"
  • Create ExecutionTask object
  • Add to asyncio queue
  ↓

LAYER 3 (Business Logic - ExecutionEngine):
  • Consume task from queue
  • Notify frontend via WebSocket: "campaign_started"
  • For each lead in scenario:
    1. Call NotionSync: fetch lead data
    2. Call GeminiService: analyze & generate message
    3. Call DevicePoolManager: pick device
    4. Prepare agent execution
  ↓

LAYER 3 (Business Logic - DevicePoolManager):
  • Check device pool health (ADB ping all devices)
  • Pick device with lowest queue (load balancing)
  • Add task to device's execution queue
  ↓

LAYER 4 (Agent - MAXAgent):
  • Initialize ADB connection to assigned device
  • Execute steps:
    • Step 1: Open MAX app (with HumanTiming pause)
    • Step 2: Find contact (HumanBehavior in action)
    • Step 3: Type message (HumanTyping with errors + pauses!)
    • Step 4: Send (HumanTiming pause before click)
    • Step 5: Validate (screenshot + check delivery)
  ↓

LAYER 5 (Hardware):
  • Device executes all steps
  • Takes screenshot at validation
  • Returns success/failure status
  ↓

LAYER 3 (Business Logic - ExecutionEngine):
  • Receive result from agent
  • If success:
    - Log to SQLite
    - Update Notion (status='sent', sent_via_max=✓)
    - Queue screenshot for saving
  • If failure:
    - Log error to SQLite
    - Update Notion (status='failed', error_message)
    - Try fallback channel (SMS, WhatsApp)
  ↓

LAYER 3 (Business Logic - TelegramLogger):
  • Batch logs (every 30 sec or when campaign complete)
  • Send to Telegram: "✓ Lead Name → MAX sent at 22:45"
  ↓

LAYER 2 (API Gateway):
  • WebSocket broadcast to all connected frontends
  • Send progress update: {completed: 5, total: 10, status: "running"}
  ↓

LAYER 1 (Frontend):
  • Zustand receives WebSocket update
  • React re-renders Dashboard
  • User sees: 5/10 completed (progress bar)
```

---

## Error Handling Flow

```
Error occurs at any layer:

LAYER 4 (Agent) - Error during send:
  • Catch exception (e.g., contact not found)
  • Return {status: "failed", error: "contact_not_found"}
  ↓

LAYER 3 (ExecutionEngine):
  • Receive failed result
  • Decision tree:
    1. If error is "device_offline" → assign to different device
    2. If error is "ui_not_recognizable" → try Gemini Vision
    3. If error is "contact_not_found" → try alternative channels
    4. If error is "rate_limit" → queue for later
    5. If error is persistent → mark task as "failed", notify user
  ↓

LAYER 3 (TelegramLogger):
  • Send alert: "⚠️ Lead Name → MAX failed: contact_not_found"
  ↓

LAYER 3 (NotionSync):
  • Update Notion: status='failed', error_message='contact_not_found'
  ↓

LAYER 1 (Frontend):
  • WebSocket update: show red "Failed" status
  • User sees: "Failed: contact not found"
```

---

## State Management

### Global State (Zustand)

```
AppStore:
  • currentScenario: Scenario | null
  • scenarios: Scenario[]
  • devices: Device[] (20 devices)
  • tasks: Task[] (current + completed)
  • executionProgress: {completed, total, status}
  • uiState: {selectedDevice, showLogs, activeTab}
  • apiConnected: boolean (WebSocket connected?)
  
Actions:
  • loadScenarios()
  • runScenario(id)
  • pauseCampaign()
  • resumeCampaign()
  • stopCampaign()
  • selectDevice(id)
  • updateDeviceStatus(id, status)
```

### Local State (Component)

```
Dashboard:
  • selectedDevice: string | null
  • expandedCards: Set<string> (which devices expanded?)
  
DeviceCard:
  • showDetails: boolean
  • showScreenshots: boolean
  
LogsViewer:
  • filterLevel: "all" | "error" | "warning" | "info"
  • searchText: string
  • autoScroll: boolean
```

---

## Concurrency Model

### AsyncIO Event Loop (Backend)

```
Main loop (runs on single thread, Python asyncio):
  1. Accept WebSocket connections
  2. Consume tasks from queue
  3. Execute 3 tasks in parallel (max)
  4. Queue remaining tasks (FIFO)
  5. Monitor device health every 30 sec
  6. Poll Notion every 60 sec
  
MAX 3 CONCURRENT EXECUTIONS across all 20 devices.
Other tasks wait in queue.
```

### Per-Device Sequential Execution

```
Device 1: Task A (60 sec) → Task B (45 sec) → wait
Device 2: Task C (70 sec) → wait
Device 3: Task D (55 sec) → wait
Device 4-20: idle

After Device 1 finishes Task A:
  → Start next queued task (Task E)

Max concurrent: 3 active, others queued.
```

---

## Performance Characteristics

| Operation | Time | Bottleneck |
|-----------|------|-----------|
| Message send (full cycle) | 60-70 sec | Device execution (HumanBehavior) |
| Notion fetch (1 lead) | 1-2 sec | Network latency |
| Gemini analysis | 2-5 sec | Gemini API latency |
| Device health check | <1 sec | ADB command |
| Screenshot save | <2 sec | Disk I/O |
| WebSocket broadcast | <100 ms | Network |
| SQLite write | <50 ms | Disk I/O |

### Throughput

```
20 devices × 30 messages/day = 600 messages/day (theoretical max)
But actual: 200-300/day (respecting rate limits + safety margins)

Per hour: 200/8 = 25 messages/hour = 1 message every 2.4 minutes
This is sustainable and doesn't trigger bot detection.
```

---

## Deployment Architecture

```
All on Mac (single machine):
  • Frontend: React dev server (Vite)
  • Backend: FastAPI server
  • Database: SQLite (local file)
  • Logs: File-based (Loguru)
  • Cache: In-memory (no Redis needed for single-machine)

No cloud services (except external APIs):
  • Notion API (read/write leads)
  • Gemini 3 Pro API (analyze leads)
  • Telegram Bot API (send notifications)

All Android devices:
  • Physically connected to Mac via USB hub
  • No remote access needed
  • All communication via local ADB
```

---

## Security Boundaries

```
┌─ TRUSTED: Local USB Bus
│   • ADB connections (USB-only, no network)
│   • Direct device control
│   • No encryption needed (local)
│
├─ SEMI-TRUSTED: Local Network (Mac)
│   • Frontend ← → Backend (localhost:8000)
│   • HTTP (not HTTPS, but local)
│   • SQLite database file (unencrypted)
│   • Logs on disk (plain text)
│
└─ UNTRUSTED: Public Internet
    • Notion API (HTTPS, API key in .env)
    • Gemini API (HTTPS, API key in .env)
    • Telegram Bot API (HTTPS, token in .env)
    • RusProfile (scraping, HTTPS)
```

---

## Monitoring & Observability

### Metrics Tracked

```
Device Metrics (per device, every 30 sec):
  • Status: OK, SLOW, OFFLINE, MAINTENANCE_NEEDED
  • Battery level (0-100%)
  • Messages sent today (0-30)
  • Last activity timestamp
  • Error count (this hour)
  
Task Metrics (per execution):
  • Start time, end time, duration
  • Status: pending, running, completed, failed
  • Error type (if failed)
  • Screenshots count
  
System Metrics (global):
  • Total messages sent (today)
  • Success rate (%)
  • Error rate (%)
  • Average send time
  • Queue size (pending tasks)
  • Concurrent executions (0-3)
```

### Logging Strategy

```
SQLite (all actions):
  • structured logs table
  • queryable by task_id, device_id, timestamp
  • retention: 30 days
  
Loguru (console + file):
  • real-time visibility
  • colored output
  • rotation every 10 MB
  
Telegram (critical alerts):
  • device offline
  • message failed
  • captcha detected
  • campaign complete
```

---

## End of 10_SYSTEM_ARCHITECTURE.md

Эта архитектура = основа всей системы. Все остальные файлы ссылаются на эту диаграмму.
