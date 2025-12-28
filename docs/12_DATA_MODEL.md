# 🗄️ DATA MODEL: Database Schema & Data Structures

## SQLite Database Schema

### Table 1: scenarios (Workflow Definitions)

```
CREATE TABLE scenarios (
  id TEXT PRIMARY KEY,              -- UUID
  name TEXT NOT NULL,               -- "Campaign Alpha"
  description TEXT,                 -- "Send to 100 new leads"
  status TEXT NOT NULL,             -- pending, active, paused, completed
  workflow_dag JSON NOT NULL,       -- DAG structure (see below)
  channel_priority TEXT,            -- "max,sms,whatsapp" (order)
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by TEXT DEFAULT "user",   -- Always "user" (no multi-user)
  notes TEXT
);

Example workflow_dag JSON:
{
  "nodes": [
    {"id": "fetch_leads", "type": "fetch_notion", "params": {"limit": 50}},
    {"id": "analyze_leads", "type": "gemini_analyze", "params": {"model": "gemini-pro"}},
    {"id": "send_messages", "type": "send_via_channels", "params": {"timeout": 70}}
  ],
  "edges": [
    {"from": "fetch_leads", "to": "analyze_leads"},
    {"from": "analyze_leads", "to": "send_messages"}
  ]
}
```

### Table 2: devices (Device Pool Management)

```
CREATE TABLE devices (
  id TEXT PRIMARY KEY,              -- "device-01", "device-02", etc
  name TEXT NOT NULL,               -- "Pixel 5 #1"
  model TEXT,                       -- "Google Pixel 5"
  android_version TEXT,             -- "14.0"
  adb_serial TEXT,                  -- "R3CR50ABC123"
  adb_ip TEXT,                      -- "192.168.1.100"
  adb_port INTEGER DEFAULT 5555,    -- TCP port
  status TEXT DEFAULT "ok",         -- ok, slow, offline, maintenance_needed
  battery_level INTEGER,            -- 0-100
  last_activity TIMESTAMP,          -- When last command ran
  last_error TEXT,                  -- Last error message
  error_count INTEGER DEFAULT 0,    -- Errors in last hour
  messages_today INTEGER DEFAULT 0, -- Counter for rate limiting
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_connected TIMESTAMP
);

Indexes:
  CREATE INDEX idx_devices_status ON devices(status);
```

### Table 3: tasks (Execution Tasks/Leads)

```
CREATE TABLE tasks (
  id TEXT PRIMARY KEY,              -- UUID
  scenario_id TEXT NOT NULL,        -- FK to scenarios
  lead_id TEXT,                     -- ID from Notion
  lead_name TEXT,                   -- "Иван Петров"
  lead_phone TEXT,                  -- "+7-999-123-45-67"
  lead_company TEXT,                -- "ООО ТДБаза"
  lead_data JSON,                   -- Full lead object from Notion
  
  status TEXT DEFAULT "pending",    -- pending, processing, sent, failed, confirmed
  assigned_device TEXT,             -- FK to devices (current executor)
  assigned_channel TEXT,            -- "max", "sms", "whatsapp"
  
  message_generated JSON,           -- {text, confidence, flags}
  message_sent TEXT,                -- Actual message sent
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  started_at TIMESTAMP,             -- When execution began
  completed_at TIMESTAMP,           -- When execution finished
  
  retry_count INTEGER DEFAULT 0,    -- How many retries
  max_retries INTEGER DEFAULT 2,
  
  error_message TEXT,               -- Why it failed
  error_type TEXT,                  -- contact_not_found, timeout, etc
  
  screenshot_path TEXT,             -- Path to saved screenshot
  notion_updated BOOLEAN DEFAULT FALSE  -- Synced back to Notion?
  
  FOREIGN KEY (scenario_id) REFERENCES scenarios(id),
  FOREIGN KEY (assigned_device) REFERENCES devices(id)
);

Indexes:
  CREATE INDEX idx_tasks_status ON tasks(status);
  CREATE INDEX idx_tasks_scenario ON tasks(scenario_id);
  CREATE INDEX idx_tasks_device ON tasks(assigned_device);
  CREATE INDEX idx_tasks_created ON tasks(created_at DESC);
```

### Table 4: executions (Detailed Step Logs)

```
CREATE TABLE executions (
  id TEXT PRIMARY KEY,              -- UUID
  task_id TEXT NOT NULL,            -- FK to tasks
  device_id TEXT NOT NULL,          -- FK to devices
  step_index INTEGER,               -- 0, 1, 2, etc (step number)
  step_name TEXT,                   -- "open_app", "find_contact", "type_message"
  step_type TEXT,                   -- launch_app, uiautomator, adb_shell, etc
  
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  duration_ms INTEGER,              -- How long step took
  
  result TEXT,                      -- "success", "failed", "timeout"
  error_message TEXT,
  
  action_details JSON,              -- Detailed log of what happened
  screenshot_before TEXT,           -- Path to before screenshot
  screenshot_after TEXT,            -- Path to after screenshot
  
  human_behavior_injected JSON,     -- {delay_ms, error_injected, backspace_count}
  
  FOREIGN KEY (task_id) REFERENCES tasks(id),
  FOREIGN KEY (device_id) REFERENCES devices(id)
);

Indexes:
  CREATE INDEX idx_executions_task ON executions(task_id);
  CREATE INDEX idx_executions_device ON executions(device_id);
  CREATE INDEX idx_executions_step ON executions(step_name);
```

### Table 5: logs (Structured Logging)

```
CREATE TABLE logs (
  id TEXT PRIMARY KEY,              -- UUID
  task_id TEXT,                     -- FK to tasks (nullable for system logs)
  device_id TEXT,                   -- FK to devices (nullable)
  
  level TEXT NOT NULL,              -- "INFO", "WARNING", "ERROR", "CRITICAL"
  message TEXT NOT NULL,            -- Log message
  module TEXT,                      -- Where log came from
  function TEXT,                    -- Function name
  
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  metadata JSON,                    -- Extra context {duration, retry_count, etc}
  
  FOREIGN KEY (task_id) REFERENCES tasks(id),
  FOREIGN KEY (device_id) REFERENCES devices(id)
);

Indexes:
  CREATE INDEX idx_logs_level ON logs(level);
  CREATE INDEX idx_logs_timestamp ON logs(timestamp DESC);
  CREATE INDEX idx_logs_task ON logs(task_id);
  CREATE INDEX idx_logs_device ON logs(device_id);
```

### Table 6: rate_limits (Per-Device Rate Limiting)

```
CREATE TABLE rate_limits (
  id TEXT PRIMARY KEY,              -- UUID
  device_id TEXT NOT NULL,          -- FK to devices
  
  hour_bucket TEXT NOT NULL,        -- "2025-01-27T22:00" (hour)
  messages_sent INTEGER DEFAULT 0,  -- Count in this hour
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  UNIQUE(device_id, hour_bucket),
  FOREIGN KEY (device_id) REFERENCES devices(id)
);

Indexes:
  CREATE INDEX idx_ratelimit_device ON rate_limits(device_id);
  CREATE INDEX idx_ratelimit_hour ON rate_limits(hour_bucket);
```

### Table 7: ui_paths (UIAutomator Paths & Selectors)

```
CREATE TABLE ui_paths (
  id TEXT PRIMARY KEY,              -- UUID
  app_name TEXT NOT NULL,           -- "max", "whatsapp", "sms"
  app_version TEXT,                 -- "8.5", "2.25", etc
  element_name TEXT NOT NULL,       -- "send_button", "message_field", "search_box"
  
  selector_type TEXT,               -- "resource_id", "text", "xpath", "content_desc"
  selector_value TEXT NOT NULL,     -- "com.alibaba.mobileim:id/send"
  
  fallback_selector JSON,           -- [{type, value}, {type, value}]
  coordinates_fallback JSON,        -- {x, y} if selector fails
  
  updated_at TIMESTAMP,
  status TEXT DEFAULT "active",     -- active, deprecated, testing
  success_rate FLOAT DEFAULT 1.0,   -- Percentage of successful finds
  
  notes TEXT
);

Indexes:
  CREATE INDEX idx_uipaths_app ON ui_paths(app_name, app_version);
  CREATE INDEX idx_uipaths_element ON ui_paths(app_name, element_name);
```

### Table 8: session_cache (Optional, for stateless API)

```
CREATE TABLE session_cache (
  key TEXT PRIMARY KEY,
  value TEXT,                       -- JSON serialized value
  expires_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Purpose: Cache frequently accessed data
Examples:
  • devices_pool_status (all device statuses)
  • gemini_context_cache (20 .md files hashes)
  • notion_sync_state (last sync time, ids already processed)
```

---

## Pydantic Models (Backend Type Definitions)

### Scenario Model

```python
class ScenarioStep(BaseModel):
    id: str
    type: str  # "fetch_notion", "gemini_analyze", "send_via_channels"
    params: Dict[str, Any]

class ScenarioDAG(BaseModel):
    nodes: List[ScenarioStep]
    edges: List[Tuple[str, str]]  # (from_id, to_id)

class Scenario(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    status: str  # "pending", "active", "paused", "completed"
    workflow_dag: ScenarioDAG
    channel_priority: str  # "max,sms,whatsapp"
    created_at: datetime
    updated_at: datetime
    created_by: str = "user"
    notes: Optional[str] = None
```

### Device Model

```python
class Device(BaseModel):
    id: str
    name: str
    model: str
    android_version: str
    adb_serial: str
    adb_ip: Optional[str] = None
    adb_port: int = 5555
    status: str  # "ok", "slow", "offline", "maintenance_needed"
    battery_level: Optional[int] = None
    last_activity: Optional[datetime] = None
    last_error: Optional[str] = None
    error_count: int = 0
    messages_today: int = 0
    
    @computed_field
    @property
    def is_available(self) -> bool:
        return self.status == "ok" and self.battery_level > 10

class DevicePool(BaseModel):
    devices: List[Device]
    total: int
    available: int
    offline: int
    slow: int
```

### Task Model

```python
class TaskResult(BaseModel):
    status: str  # "success", "failed", "timeout"
    message: Optional[str] = None
    screenshot_path: Optional[str] = None
    duration_seconds: float

class Task(BaseModel):
    id: str
    scenario_id: str
    lead_id: str
    lead_name: str
    lead_phone: str
    lead_company: str
    
    status: str  # "pending", "processing", "sent", "failed", "confirmed"
    assigned_device: Optional[str] = None
    assigned_channel: Optional[str] = None
    
    message_generated: Optional[Dict[str, Any]] = None
    message_sent: Optional[str] = None
    
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    retry_count: int = 0
    error_message: Optional[str] = None
    error_type: Optional[str] = None
    screenshot_path: Optional[str] = None
    notion_updated: bool = False
```

### Execution Model

```python
class ExecutionStep(BaseModel):
    id: str
    task_id: str
    device_id: str
    step_index: int
    step_name: str
    step_type: str
    
    result: str  # "success", "failed", "timeout"
    error_message: Optional[str] = None
    duration_ms: int
    
    screenshot_before: Optional[str] = None
    screenshot_after: Optional[str] = None
    
    human_behavior_injected: Optional[Dict[str, Any]] = None
```

---

## Notion CRM Database Schema

### Leads Table (Row Structure)

```
Column 1: ID
  Type: Unique identifier
  Example: "notion_123abc"

Column 2: Full Name
  Type: Text
  Example: "Иван Петров"

Column 3: Company
  Type: Text
  Example: "ООО ТДБаза"

Column 4: Phone
  Type: Text
  Example: "+7-999-123-45-67"

Column 5: Website
  Type: URL
  Example: "https://example.ru"

Column 6: RusProfile URL
  Type: URL
  Example: "https://rusprofile.ru/id/123456"

Column 7: Revenue
  Type: Number (rubles)
  Example: 7000000

Column 8: Profit
  Type: Number (rubles)
  Example: 500000

Column 9: Status
  Type: Select
  Options: pending, processing, sent, failed, confirmed

Column 10: Sent via MAX
  Type: Checkbox
  Example: ✓ (checked = already sent)

Column 11: Sent via SMS
  Type: Checkbox
  Example: ☐ (unchecked = not sent)

Column 12: Sent via WhatsApp
  Type: Checkbox
  Example: ☐

Column 13: Last Message
  Type: Text (long)
  Example: "Иван, видел что у вас выручка 7млн..."

Column 14: Response
  Type: Text
  Example: "Спасибо, интересно!"

Column 15: Response Date
  Type: Date
  Example: 2025-01-27

Column 16: Notes
  Type: Text
  Example: "Follow up next week"

Column 17: Created Date
  Type: Created time (auto)

Column 18: Last Updated
  Type: Last edited time (auto)
```

---

## JSON Data Structures

### Message Generation Result (from Gemini)

```json
{
  "text": "Иван, видел что у вас выручка 7млн в год. Может быть полезна автоматизация процессов, которые сейчас отнимают время. Когда удобно обсудить детали?",
  "confidence": 0.92,
  "flags": [],
  "tone": "professional",
  "language": "russian"
}
```

### HumanBehavior Injection Data

```json
{
  "typing_delays": {
    "per_char_ms": [80, 95, 200, 85, 90, ...],
    "pause_before_punctuation": 300,
    "pause_between_words": [100, 150, 120, ...],
    "total_time_sec": 45
  },
  "errors_injected": [
    {"position": 15, "wrong_char": "з", "correct_char": "с", "backspace_count": 1}
  ],
  "action_delays": {
    "before_click": 350,
    "after_click": 500,
    "before_scroll": 200
  }
}
```

### Execution Log Entry

```json
{
  "task_id": "task-123",
  "device_id": "device-01",
  "timestamp": "2025-01-27T22:45:30Z",
  "level": "INFO",
  "message": "Message sent successfully",
  "step": "send_message",
  "metadata": {
    "duration_sec": 65,
    "retry_count": 0,
    "human_behavior_applied": true,
    "screenshot_size_kb": 650
  }
}
```

---

## Data Relationships (E/R Diagram)

```
Scenario (1) ──────→ (many) Task
  │
  └─→ Task (1) ──────→ (many) Execution
        │
        ├─→ (1) Device (assigned_device)
        └─→ (many) Execution
              │
              ├─→ (1) Device
              └─→ (many) Log

Device (1) ──────→ (many) Task
  │
  └─→ (many) Execution
  └─→ (many) Log
  └─→ (many) RateLimit

Task (1) ──────→ (many) Execution
  │
  └─→ (many) Log

UIPath (1) ──────→ (1) App Version
```

---

## Data Retention & Cleanup Policies

```
Logs Table:
  • Keep: 30 days
  • Delete: Older than 30 days
  
Screenshots:
  • Keep: 7 days
  • Delete: Older than 7 days
  • Max storage: 50 GB
  
Completed Tasks:
  • Keep: Forever
  • Archive: None (SQLite is local, not huge)
  
Execution Details:
  • Keep: 7 days (linked to task)
  • Delete: If task deleted
  
Session Cache:
  • Keep: Until expires_at
  • Auto-cleanup: On insert/query
```

---

## Backup & Recovery

```
SQLite Database:
  • File: /path/to/database.db
  • Backup frequency: Daily (automated)
  • Backup location: /path/to/backups/db_YYYYMMDD.db
  • Retention: 30 days
  
Screenshots:
  • Location: /data/screenshots/
  • Backup: Weekly to external drive
  • Retention: 7 days (live), 30 days (archived)
  
Recovery:
  • If database corrupt: restore from backup
  • If task failed: can rerun with same lead
  • If device offline: requeue task to different device
```

---

## End of 12_DATA_MODEL.md

Полная схема базы данных + все модели данных.

Готов создать **файл 13 (Device Topology - Локальная)**?
