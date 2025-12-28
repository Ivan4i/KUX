# Android Agent Platform - Roadmap

**Дата создания:** 2025-12-03
**Статус:** В разработке - Slice 1
**MVP Цель:** Desktop приложение для автоматизации WhatsApp через 3 Google Pixel 5 устройства

---

## 🎯 Общая Цель

Создать production-ready desktop приложение для автоматизации WhatsApp рассылок через удаленные Android устройства, подключенные через VPN (Tailscale + ADB).

**Подход:** Вертикальные срезы - каждый slice это полностью рабочий продукт.

**Технологии:**
- Backend: Python 3.11+ (FastAPI, SQLAlchemy, AsyncIO)
- Frontend: React 18+ (TypeScript, Vite, TailwindCSS)
- LLM: Puter.js (Claude Sonnet 4.5 / Gemini 3 Pro / GPT 5.1)
- Database: SQLite → PostgreSQL
- Android: DroidRun + uiautomator2

---

## 📅 Timeline

| Slice | Длительность | Статус | Дата начала | Дата окончания |
|-------|--------------|--------|-------------|----------------|
| **Slice 1** | 5-7 дней | 🟡 В работе | 2025-12-03 | - |
| **Slice 2** | 7 дней | ⚪ Не начато | - | - |
| **Slice 3** | 7 дней | ⚪ Не начато | - | - |
| **Polish** | 7-9 дней | ⚪ Не начато | - | - |

---

## 🎯 SLICE 1: Минимальный WhatsApp Flow (MVP)

**Цель:** Отправить 1-2 WhatsApp сообщения с одного Pixel устройства через простой UI.

### Функциональность

**Backend:**
- ✅ Device Manager подключается к 1 Pixel через ADB over Tailscale
- ✅ WhatsApp Agent отправляет сообщение (открывает WhatsApp, находит контакт, печатает, отправляет)
- ✅ Notion Integration читает 2 задачи из таблицы `WhatsApp_Outreach`
- ✅ Puter.js LLM генерирует персонализированные сообщения
- ✅ Telegram Bot отправляет info уведомления
- ✅ SQLite сохраняет логи (Device, Task, Log таблицы)
- ✅ WebSocket отправляет real-time updates в UI
- ✅ API endpoints: `/api/devices`, `/api/tasks`, `/api/logs`

**Frontend:**
- ✅ Dashboard Page с Device Card, Current Activity, Recent Logs
- ✅ Buttons: "Sync Notion", "Run Task"
- ✅ Real-time updates через WebSocket
- ✅ V3 Design System компоненты

### Критические Файлы

**Backend (Python):**
```
backend/src/
├── main.py                              # FastAPI entry point
├── device_manager/
│   ├── manager.py                       # DeviceManager класс
│   └── adb_handler.py                   # ADB команды
├── agents/
│   ├── base_agent.py                    # BaseAgent
│   ├── whatsapp_agent.py                # WhatsApp logic
│   └── droidrun_wrapper.py              # DroidRun + uiautomator2
├── behaviors/
│   ├── human_typing.py                  # Typing emulation
│   └── human_timing.py                  # Timing delays
├── integrations/
│   ├── notion_client.py                 # Notion API
│   ├── puter_client.py                  # Puter.js API
│   └── telegram_bot.py                  # Telegram Bot
├── database/
│   ├── db.py                            # SQLite setup
│   ├── models.py                        # ORM models
│   └── schemas.py                       # Pydantic schemas
├── routes/
│   ├── devices.py                       # Device API
│   ├── tasks.py                         # Task API
│   └── logs.py                          # Logs API
└── websocket/
    └── manager.py                       # WebSocket manager
```

**Frontend (React + TypeScript):**
```
frontend/src/
├── main.tsx                             # Entry point
├── App.tsx                              # Main app
├── pages/
│   └── DashboardPage.tsx                # Dashboard
├── components/
│   ├── common/
│   │   ├── Button.tsx                   # V3 Button
│   │   └── Card.tsx                     # V3 Card
│   └── dashboard/
│       ├── DeviceCard.tsx               # Device status
│       ├── CurrentActivity.tsx          # Current task
│       └── RecentLogs.tsx               # Logs list
├── hooks/
│   ├── useWebSocket.ts                  # WebSocket hook
│   └── useApi.ts                        # API hook
├── services/
│   ├── api.ts                           # API client
│   └── websocket.ts                     # WebSocket client
├── styles/
│   └── theme.ts                         # V3 Design tokens
└── types/
    ├── device.ts                        # Device types
    └── task.ts                          # Task types
```

### Success Criteria (Slice 1)

✅ Когда можно считать Slice 1 завершенным:
- [ ] 1 Pixel online и виден в Dashboard
- [ ] 2 сообщения успешно отправлены через WhatsApp
- [ ] Real-time updates работают в UI
- [ ] Notion синхронизируется (Status: Pending → Sent)
- [ ] Telegram уведомления приходят

---

## 🚀 SLICE 2: Full WhatsApp Flow (Production-Ready)

**Цель:** Production-ready WhatsApp с очередями, retries, human behavior.

**Длительность:** 7 дней

### Добавить к Slice 1

**Backend Additions:**
1. **Queue Manager** - Priority queue, device assignment, concurrent execution
2. **Retry Manager** - Retry logic с exponential backoff (max 3 attempts)
3. **Recovery Agent** - 5 уровней восстановления (retry → alternative → restart → reboot → manual)
4. **Enhanced Human Behavior** - Typos (5%), warmup mode (< 7 days: max 5 msgs/day), active hours (8am-10pm)
5. **Background Notion Sync** - Auto-sync каждые 60 сек, batch updates
6. **Enhanced Telegram Bot** - INFO/WARNING/ERROR alerts, interactive buttons
7. **Task Scheduler** - Cron-like scheduler для recurring tasks
8. **Health Monitor** - Battery/temperature/RAM monitoring каждые 60 сек

**Frontend Additions:**
1. **Dashboard Enhancements** - 3 Device Cards, queue visualizer
2. **Tasks Page** - Active/Queued/Completed sections, filtering
3. **Logs Page** - Advanced filtering, search, export CSV
4. **Toast Notifications** - Real-time toast + desktop notifications

### Success Criteria (Slice 2)

✅ Когда можно считать Slice 2 завершенным:
- [ ] 3 Pixel'я работают параллельно
- [ ] 20+ задач обрабатываются с очередью
- [ ] Retry logic работает при ошибках
- [ ] Human behavior включен (typos, delays, warmup)
- [ ] Daily summary приходит в Telegram в 21:00

---

## 🎨 SLICE 3: Scenario Builder (Advanced Features)

**Цель:** Visual drag-and-drop конструктор для multi-step сценариев.

**Длительность:** 7 дней

### Добавить к Slice 2

**Backend Additions:**
1. **Scenario Models** - Scenario + ScenarioExecution ORM models
2. **Scenario Runner** - Step-by-step execution engine (whatsapp, wait, conditional, recovery)
3. **Scenario API** - Full CRUD + run/schedule endpoints

**Frontend Additions:**
1. **Scenarios Page** - Список всех сценариев
2. **Scenario Builder** - Visual DnD constructor (3 columns: Actions, Constructor, Editor)
3. **Action Menu** - Draggable actions (WhatsApp, Wait, Conditional, Recovery)
4. **Step Card** - Visual step representation
5. **Step Editor** - Dynamic form для настройки шага
6. **Scenario Card** - Summary карточка с actions

### Success Criteria (Slice 3)

✅ Когда можно считать Slice 3 завершенным:
- [ ] Визуальный конструктор работает (DnD)
- [ ] Сценарий с 3+ шагами создан и выполнен
- [ ] Scheduled scenarios автоматически запускаются
- [ ] Execution history сохраняется и отображается

---

## ⚠️ Риски и Митигации

### High Priority

**1. ADB over Tailscale Stability**
- Auto-reconnect logic (60 сек heartbeat)
- Connection quality monitoring

**2. WhatsApp UI Changes**
- DroidRun (адаптивный AI agent)
- Fallback на uiautomator2
- Version lock WhatsApp APK

**3. Account Blocking**
- Human behavior layer
- Warmup mode (5 msgs/day первую неделю)
- Active hours (8am-10pm), weekend slowdown

**4. LLM API Rate Limits**
- Caching responses
- Fallback на templates
- Retry с backoff

**5. Notion API Rate Limits**
- Batch updates (5-10 задач)
- Local caching (sync каждые 60 сек)

---

## 📝 Важные Заметки

### Puter.js API - КРИТИЧЕСКИ ВАЖНО!

**Всегда указывать модель при запросе:**

```python
# ✅ ПРАВИЛЬНО
response = await puter_client.generate(
    prompt="Generate message...",
    model="claude-sonnet-4.5"  # или "gemini-3-pro" или "gpt-5.1"
)

# ❌ НЕПРАВИЛЬНО (отправит на дешевую модель!)
response = await puter_client.generate(prompt="...")
```

### Notion Table Structure

Таблица `WhatsApp_Outreach`:
- Message ID (unique)
- Recipient Name
- Phone Number
- Message Content
- Status (Pending / Sent / Failed)
- Device Assignment (Auto / Pixel-TH-1 / ...)
- Priority (1-10)
- Created Date, Sent Date, Attempt Count, Notes

### Device Configuration

Файл `/config/devices.yaml`:
```yaml
devices:
  - id: pixel-th-1
    name: Pixel-TH-1
    location: Bangkok, Thailand
    timezone: Asia/Bangkok
    tailscale_ip: 100.64.1.101
    adb_port: 5555
    active_hours: "08:00-22:00"
    max_tasks_per_day: 50

  - id: pixel-vn-1
    name: Pixel-VN-1
    location: Ho Chi Minh, Vietnam
    timezone: Asia/Ho_Chi_Minh
    tailscale_ip: 100.64.1.102
    adb_port: 5555
    active_hours: "08:00-22:00"
    max_tasks_per_day: 50

  - id: pixel-th-2
    name: Pixel-TH-2
    location: Bangkok, Thailand
    timezone: Asia/Bangkok
    tailscale_ip: 100.64.1.103
    adb_port: 5555
    active_hours: "08:00-22:00"
    max_tasks_per_day: 30
```

---

## 📚 Ссылки на Документацию

- **IDEAL_VISION.md** - Полное видение проекта
- **IMPLEMENTATION_GUIDE.md** - Детальное руководство реализации
- **V3-DESIGN_SYSTEM.md** - Дизайн-система (для UI компонентов)
- **promt-dev-base.md** - Принципы разработки и стандарты
- **PROGRESS.md** - Текущий прогресс (обновляется в реальном времени)

---

## 🎯 Следующие Шаги

**Текущий этап:** Slice 1 - Минимальный WhatsApp Flow

**Сейчас в работе:**
1. Создание структуры проекта (backend, frontend, scripts, config)
2. Setup backend environment (Python venv, requirements.txt, .env)

**Следующие задачи:**
- Device Manager реализация
- WhatsApp Agent реализация
- Integrations (Notion, Puter.js, Telegram)

---

*Этот roadmap обновляется по мере прогресса разработки. Смотри PROGRESS.md для детального статуса.*
