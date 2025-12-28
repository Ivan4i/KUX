# IDEAL VISION — Android Agent Platform

## Описание проекта в целом

Это **локальное desktop приложение**, которое запускается на твоём ПК (Windows/Mac/Linux) и полностью управляет тремя Google Pixel 5 устройствами, находящимися физически в Таиланде и Вьетнаме через защищённое VPN-соединение (Tailscale + ADB).

**Что платформа делает:**
- Автоматизирует WhatsApp рассылки (персонализированные сообщения клиентам)
- Управляет LinkedIn активностью (лайки, подписки, комментарии)
- Публикует Instagram Reels (видеоконтент)
- Эмулирует человеческое поведение (задержки, ошибки, неправильные ритмы)
- Интегрируется с Notion базой данных
- Отправляет уведомления в Telegram бот
- Использует Gemini 3 Pro LLM для умных решений
- Имеет красивый UI, следуя твоей дизайн-системе

**Главное отличие от GeeLark:**
- 100% твой контроль (не облачная платформа)
- Полная кастомизация логики
- Масштабируемость (легко добавить 10 телефонов)
- Можно коммерциализировать и продавать

---

## ЧАСТЬ 1: ПОЛЬЗОВАТЕЛЬСКИЙ ИНТЕРФЕЙС (UI/UX)

### 1.1 Главный экран (Dashboard)

Когда пользователь открывает приложение, видит:

**Сверху (Header):**
- Логотип приложения слева
- Текущее время и дата
- Кнопка Settings (иконка ⚙️ из Boxicons)
- Кнопка Help (иконка ❓)
- Кнопка About (иконка ℹ️)

**Левая боковая панель (Sidebar) — 25% ширины:**
```
┌─────────────────────────┐
│  ANDROID AGENT          │
│                         │
│  📊 Dashboard           │
│  🎯 Scenarios           │
│  📱 Devices             │
│  📋 Tasks               │
│  📊 Analytics           │
│  📝 Logs                │
│  ⚙️ Settings            │
│                         │
│ ━━━━━━━━━━━━━━━━━━━━━  │
│ System Status:          │
│ ✅ All devices online   │
│ ✅ Notion connected     │
│ ✅ Telegram ready       │
│ ✅ Gemini API OK        │
└─────────────────────────┘
```

**Центральная часть (Main Content) — 75% ширины:**

#### Блок 1: Device Status Cards (вверху)
Три карточки горизонтально, каждая 30% ширины с gap между ними:

```
┌─────────────────────────┬─────────────────────────┬─────────────────────────┐
│ 🟢 Pixel-TH-1          │ 🟢 Pixel-VN-1          │ 🟡 Pixel-TH-2          │
│                         │                         │                         │
│ Battery: 85% 🔋        │ Battery: 92% 🔋        │ Battery: 78% 🔋        │
│ Temp: 32°C 🌡️         │ Temp: 29°C 🌡️         │ Temp: 25°C 🌡️         │
│ RAM: 60% 📊            │ RAM: 55% 📊            │ RAM: 40% 📊            │
│ Signal: 📶📶           │ Signal: 📶📶📶        │ Signal: - (sleeping)    │
│ Status: Working        │ Status: Working        │ Status: Sleeping       │
│ Task: WA (7/10)        │ Task: None             │ Task: None             │
│ Last ping: 1min ago    │ Last ping: 30sec ago   │ Last ping: 45min ago   │
└─────────────────────────┴─────────────────────────┴─────────────────────────┘
```

Каждая карточка интерактивна:
- Клик на карточку → детальная информация об этом Pixel'е
- Кнопки: Restart / Reboot / Clear Cache (на каждой карточке)

#### Блок 2: Current Activity (в центре)
Большой блок, занимающий 60% ширины:

```
┌────────────────────────────────────────────────────────────────┐
│ CURRENT ACTIVITY                                               │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│ Scenario: "Morning WhatsApp Blitz"                            │
│ Device: Pixel-TH-1                                            │
│ Status: RUNNING ✅                                             │
│                                                                │
│ Current Step: WhatsApp Message #7 of 10                       │
│ Action: Typing message...                                     │
│ Recipient: Ramesh Kumar (+66812345678)                        │
│                                                                │
│ Progress: ████████░░░░░░░░░░░░░░░░ 70%                        │
│ Time elapsed: 1h 24m                                          │
│ Time remaining: ~30m                                          │
│                                                                │
│ Next action in: ⏱️ 3m 47s (Wait before next message)          │
│                                                                │
│ Pause | Resume | Stop | Detailed Logs ▼                       │
└────────────────────────────────────────────────────────────────┘
```

#### Блок 3: Recent Activity Log (справа)
30% ширины, вертикально:

```
┌──────────────────────────────────────────┐
│ RECENT ACTIVITY                          │
├──────────────────────────────────────────┤
│ ✅ 14:52 Sent message to Ramesh Kumar    │
│    +66812345678 (Message #6)             │
│                                          │
│ ⏳ 14:48 Waiting 285 seconds...          │
│                                          │
│ ✅ 14:42 Sent message to Priya Singh     │
│    +66987654321 (Message #5)             │
│                                          │
│ ⚠️  14:35 Retry: Number not found        │
│    +66111111111 (trying alternative)     │
│                                          │
│ ✅ 14:28 Sent message to Anil Patel     │
│    +66555555555 (Message #4)             │
│                                          │
│ ⏳ 14:20 Waiting 642 seconds...          │
│                                          │
│ ✅ 14:10 Sent message to Deepak Sharma   │
│    +66222222222 (Message #3)             │
│                                          │
│ ⏳ 14:02 Typing text...                  │
│                                          │
│ ✅ 13:55 Sent message to Kumar Singh    │
│    +66333333333 (Message #2)             │
│                                          │
│ [View all logs →]                        │
└──────────────────────────────────────────┘
```

Каждая запись кликабельна → показывает детали (скриншот момента, полный лог, если была ошибка).

#### Блок 4: Quick Statistics (внизу справа)
Маленькие карточки с метриками:

```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Today Stats  │ Success Rate │ Avg Duration │ Errors       │
├──────────────┼──────────────┼──────────────┼──────────────┤
│              │              │              │              │
│ Messages: 27 │ 96%          │ 45 sec/msg   │ 0 critical   │
│ LinkedIn: 8  │ ✅           │ WhatsApp     │ 1 warning    │
│ Reels: 1     │              │              │              │
│              │              │              │              │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

### 1.2 Вкладка "Scenarios" (Сценарии)

**Верхняя часть:**
- Большая кнопка "+ Create New Scenario" (зелёная, заметная)
- Кнопка "Import from template" (загрузить готовый сценарий)

**Основная часть — Список сценариев:**

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Morning WhatsApp Blitz                          ▶  Last run: 2h ago     │
│ Scheduled: Every day 08:00-11:00                                        │
│ Status: ENABLED ✅                                                       │
├──────────────────────────────────────────────────────────────────────────┤
│ Steps:                                                                   │
│   1. [WhatsApp Outreach]    10 messages                                  │
│   2. [Wait]                 2 hours (cooldown)                           │
│   3. [LinkedIn Activity]    5 likes, 3 follows                           │
│ ────────────────────────────────────────────────────────────────────────  │
│ [Edit] [Duplicate] [Run Now] [Schedule] [Delete]                        │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ Evening Reel Drop                                Last run: Yesterday     │
│ Scheduled: Daily 19:30                                                   │
│ Status: ENABLED ✅                                                       │
├──────────────────────────────────────────────────────────────────────────┤
│ Steps:                                                                   │
│   1. [Instagram Reels]      1 video from Telegram                        │
│   2. [LinkedIn Engagement]  2 minutes of activity                        │
│ ────────────────────────────────────────────────────────────────────────  │
│ [Edit] [Duplicate] [Run Now] [Schedule] [Delete]                        │
└──────────────────────────────────────────────────────────────────────────┘
```

### 1.3 Конструктор сценариев (Scenario Builder)

Когда пользователь нажимает "Create New" или "Edit":

**Левая колонка — Меню действий (Drag & Drop):**
```
AVAILABLE ACTIONS
─────────────────────────
📧 WhatsApp Outreach
   └ Send personalized messages

🔗 LinkedIn Activity
   ├ Like posts
   ├ Follow users
   └ Send messages

📸 Instagram Reels
   └ Post video from Telegram

🎯 LinkedIn Engagement
   └ Like + comment + follow

⏱️  Wait/Cooldown
   └ Pause for X minutes

🔄 Recovery Mode
   └ Clear cache, retry

❌ Conditional: If failed
   └ Do alternative action
```

**Центральная колонка — Визуальный конструктор:**
```
SCENARIO BUILDER
────────────────────────────────────────────────
Scenario Name: [____________] Morning WhatsApp Blitz

┌──────────────────────┐
│ ▶ START              │
└────────┬─────────────┘
         │
    ┌────▼───────────────────┐
    │ 📧 WhatsApp Outreach   │ ← drag-drop
    │ • Messages: 10         │   на кнопку
    │ • Device: Auto         │   Edit ✎
    │ • From: Notion         │   ⋮
    │ • Interval: 15-25min   │
    └────┬──────────────────┘
         │
    ┌────▼───────────────────┐
    │ ⏱️  Wait: 120 minutes   │ ← drag-drop
    │ • Reason: Cooldown     │   Edit ✎
    │                        │   ⋮
    └────┬──────────────────┘
         │
    ┌────▼───────────────────┐
    │ 🔗 LinkedIn Activity   │ ← drag-drop
    │ • Likes: 5             │   Edit ✎
    │ • Follows: 3           │   ⋮
    │ • Comments: 1          │
    └────┬──────────────────┘
         │ (if failed: repeat WA)
    ┌────▼───────────────────┐
    │ ❌ Conditional         │ ← drag-drop
    │ • Condition: Failed    │   Edit ✎
    │ • Action: Retry WA     │   ⋮
    └────┬──────────────────┘
         │
    ┌────▼─────────────┐
    │ ⏹ END            │
    └──────────────────┘
```

**Справа — Настройки текущего блока:**
```
STEP DETAILS: WhatsApp Outreach
──────────────────────────────────
Number of messages: [10    ]

Load from: ◉ Notion Database
           ○ Manual input
           ○ CSV file

Device Assignment:
  ○ Auto (any available)
  ◉ Pixel-TH-1
  ○ Pixel-VN-1
  ○ Pixel-TH-2

Message Interval:
  Min: [15] minutes
  Max: [25] minutes

Warmup Mode: ○ No
             ◉ Yes (account age < 7 days)

Retry Policy:
  Max attempts: [3]
  Backoff time: [5] minutes

[Save] [Cancel] [Preview]
```

**Кнопки внизу:**
- `[Save Scenario]` — сохранить
- `[Run Now]` — запустить немедленно
- `[Schedule]` — выбрать время запуска
- `[Test]` — test mode (1 сообщение, без реальной отправки)

### 1.4 Вкладка "Devices"

**Таблица со всеми Pixel'ями:**

```
┌──────────┬────────┬─────────┬──────┬───────┬─────────┬──────────────┬────────────┐
│ Device   │ Status │ Battery │ Temp │ RAM   │ Signal  │ Last Ping    │ Actions    │
├──────────┼────────┼─────────┼──────┼───────┼─────────┼──────────────┼────────────┤
│ Pixel-   │ 🟢     │ 85%     │ 32°C │ 60%   │ 📶📶   │ 1 min ago    │ Restart    │
│ TH-1     │ Online │ ⚡      │      │ 📊    │         │              │ Reboot     │
│          │        │ ⏱️      │      │       │         │              │ Clear Data │
├──────────┼────────┼─────────┼──────┼───────┼─────────┼──────────────┼────────────┤
│ Pixel-   │ 🟢     │ 92%     │ 29°C │ 55%   │ 📶📶📶 │ 30 sec ago   │ Restart    │
│ VN-1     │ Online │ ⚡      │      │ 📊    │         │              │ Reboot     │
│          │        │ ⏱️      │      │       │         │              │ Clear Data │
├──────────┼────────┼─────────┼──────┼───────┼─────────┼──────────────┼────────────┤
│ Pixel-   │ 🟡     │ 78%     │ 25°C │ 40%   │ -       │ 45 min ago   │ Wake Up    │
│ TH-2     │ Sleep  │ ⚡      │      │ 📊    │         │              │ Reboot     │
│          │        │ ⏱️      │      │       │         │              │ Clear Data │
└──────────┴────────┴─────────┴──────┴───────┴─────────┴──────────────┴────────────┘
```

**Клик на Device → детальная страница:**

```
DEVICE: Pixel-TH-1 (Bangkok)
─────────────────────────────────────────────────────

System Info:
  • Model: Google Pixel 5
  • OS: Android 14
  • RAM: 8 GB
  • Storage: 128 GB (92 GB free)
  • Tailscale IP: 100.64.1.101
  • Last Bootup: 3 days ago

Real-time Monitoring:
  • Battery: 85% (charging)
  • Temperature: 32°C
  • RAM Usage: 60% (4.8 GB of 8 GB)
  • Screen: ON
  • Internet: 4G LTE (excellent)

Active Apps:
  • WhatsApp
  • LinkedIn
  • Telegram
  • Every Proxy (SOCKS5 server)

Recent Logs (Last 24 hours):
  ✅ 14:52 Message sent to +66812345678
  ⏳ 14:48 Waiting for next action
  ✅ 14:42 Message sent to +66987654321
  ...

Actions:
  [Force Restart] [Full Reboot] [Clear App Cache] [View Full Logs]
  [SSH into Device] [Download Logs] [Health Check]
```

### 1.5 Вкладка "Tasks"

**Текущие задачи (Real-time обновление):**

```
┌───────────────────────────────────────────────────────────────────┐
│ ACTIVE TASKS (3)                                                  │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│ 📧 WhatsApp: Message 7/10 (Pixel-TH-1)                            │
│    Recipient: Ramesh Kumar (+66812345678)                        │
│    Status: SENDING ⏳                                              │
│    Progress: [███████░░░░░░░░░░░░░] 35%                           │
│    Duration: 45 seconds                                          │
│                                                                   │
│ 📊 Analytics Processing (Background)                              │
│    Task: Calculate daily metrics                                 │
│    Progress: [█████████░░░░░░░░░░░] 50%                          │
│    Duration: 2 seconds                                           │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘

QUEUED TASKS (12)
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│ Priority 1: 📧 WhatsApp Message 8/10 (Pixel-TH-1)               │
│            Est. start: 1 min 20 sec                              │
│                                                                   │
│ Priority 2: 🔗 LinkedIn Like post (Pixel-VN-1)                  │
│            Est. start: 2 min 30 sec                              │
│                                                                   │
│ Priority 3: 📧 WhatsApp Message 9/10 (Pixel-TH-1)               │
│            Est. start: 4 min 45 sec                              │
│                                                                   │
│ ... (showing top 3, total 12 queued)                             │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘

COMPLETED TODAY (27)
├───────────────────────────────────────────────────────────────────┤
│ ✅ All 27 tasks completed successfully                            │
│    Click to view details                                         │
└───────────────────────────────────────────────────────────────────┘
```

### 1.6 Вкладка "Analytics"

**Графики и статистика:**

```
ANALYTICS & METRICS
─────────────────────────────────────────────────

Last 7 Days Performance:
┌─────────────────────────────────────────────────┐
│  Success Rate by Day                            │
│  100% ┤                                         │
│       │ ██                                      │
│   75% ┤ ██  ██  ██                              │
│       │ ██  ██  ██  ██  ██  ██  ██              │
│   50% ├─────────────────────────────────────   │
│       │ Mon Tue Wed Thu Fri Sat Sun              │
│    0% ┤                                         │
└─────────────────────────────────────────────────┘

Summary:
  • Total messages sent: 189
  • Success rate: 96.8%
  • Failed messages: 6 (invalid numbers: 4, blocked: 2)
  • Average message duration: 45 seconds
  • Total time active: 18 hours

Top Errors:
  1. "Number not found" - 4 times
  2. "Account might be flagged" - 2 times
  3. "Network timeout" - 1 time

Device Utilization:
  • Pixel-TH-1: 35 hours (42%)
  • Pixel-VN-1: 32 hours (38%)
  • Pixel-TH-2: 19 hours (20%)

Export: [CSV] [JSON] [PDF]
```

### 1.7 Вкладка "Logs"

**Полный лог со фильтрацией:**

```
LOGS & DEBUGGING
─────────────────────────────────────────────────

Filters:
  Date: [Today ▼] [All Time / Last 24h / Last 7d]
  Device: [All ▼] [Pixel-TH-1 / Pixel-VN-1 / Pixel-TH-2]
  Type: [All ▼] [WhatsApp / LinkedIn / Instagram]
  Status: [All ▼] [Success / Failed / Warning / Info]
  Search: [________________]
  
  [Apply Filters] [Clear All] [Export as CSV]

Results: 247 logs found

┌─────────┬──────────────┬────────────┬────────┬──────────────────────┐
│ Time    │ Device       │ Action     │ Status │ Message              │
├─────────┼──────────────┼────────────┼────────┼──────────────────────┤
│ 14:52   │ Pixel-TH-1   │ WhatsApp   │ ✅     │ Message sent to      │
│         │              │            │        │ +66812345678         │
├─────────┼──────────────┼────────────┼────────┼──────────────────────┤
│ 14:48   │ Pixel-TH-1   │ Wait       │ ⏳     │ Waiting 285 seconds  │
├─────────┼──────────────┼────────────┼────────┼──────────────────────┤
│ 14:42   │ Pixel-TH-1   │ WhatsApp   │ ✅     │ Message sent to      │
│         │              │            │        │ +66987654321         │
├─────────┼──────────────┼────────────┼────────┼──────────────────────┤
│ 14:35   │ Pixel-TH-1   │ WhatsApp   │ ⚠️     │ Retry: Number not    │
│         │              │            │        │ found, trying again  │
└─────────┴──────────────┴────────────┴────────┴──────────────────────┘

[Showing 1-10 of 247] [Next] [Last]
```

Клик на логу → детали:
```
LOG DETAILS
─────────────────────────────────────────────────
Time: 2025-12-03 14:35:22 UTC
Device: Pixel-TH-1
Task ID: task_whatsapp_msg_6
Action Type: WhatsApp Message Send
Status: ⚠️ RETRY
Duration: 12 seconds

Details:
  Recipient: Unknown User
  Phone: +66111111111
  Message: "Hey, I saw your profile..."
  
  Step 1: Open WhatsApp - SUCCESS (2.1s)
  Step 2: Search contact - FAILED (8.2s)
  Step 3: Retry search - RETRY (1.7s)
  
  Error: Contact not found in database
  LLM Analysis: "Number might be invalid or WhatsApp UI changed"
  Screenshot: [View] [Download]
  
  Next action: Mark as invalid, move to next message

[Close] [Retry] [Manual Intervention] [Report Bug]
```

### 1.8 Вкладка "Settings"

**Конфигурация приложения:**

```
SETTINGS
─────────────────────────────────────────────────

API Keys & Credentials
├─ Notion API Key: [••••••••••••••••••] [Test]
├─ Telegram Bot Token: [••••••••••••••••••] [Test]
├─ Gemini API Key: [••••••••••••••••••] [Test]
└─ Gemini Proxy (optional): [laozhang.ai endpoint]

Device Configuration
├─ Pixel-TH-1
│  ├─ Timezone: Asia/Bangkok
│  ├─ Active Hours: 08:00 - 22:00
│  ├─ Max tasks/day: 50
│  ├─ Cooling threshold: 40°C
│  └─ [Edit]
├─ Pixel-VN-1
│  ├─ Timezone: Asia/Ho_Chi_Minh
│  ├─ Active Hours: 08:00 - 22:00
│  ├─ Max tasks/day: 50
│  ├─ Cooling threshold: 40°C
│  └─ [Edit]
└─ Pixel-TH-2
   ├─ Timezone: Asia/Bangkok
   ├─ Active Hours: 08:00 - 22:00
   ├─ Max tasks/day: 30
   ├─ Cooling threshold: 40°C
   └─ [Edit]

Behavior Settings
├─ Human Typing Speed: [Slow ←→ Fast] (defaults to ~80 chars/min)
├─ Pause Between Messages: [15] - [25] minutes
├─ Typo Frequency: [10%] (randomness)
├─ Daily Active Time: [20 hours]
├─ Maintenance Window: [03:00 - 04:00] UTC+7
└─ Account Warmup: [Enabled] (first 7 days: 5 msgs/day)

Logging & Monitoring
├─ Log Level: [Debug ▼] [Info / Warning / Error]
├─ Auto-cleanup logs older than: [30] days
├─ Screenshot on error: [✓] Enabled
├─ Local database location: [/data/sqlite.db]
└─ Backup interval: [Every 24 hours]

Notifications
├─ Telegram alerts: [✓] Critical / Warning / Info
├─ Desktop notifications: [✓] Enabled
├─ Email alerts: [  ] Disabled
└─ Daily summary: [✓] 21:00 UTC+7

[Save Changes] [Reset to Defaults] [Backup Settings] [Restore Settings]
```

---

## ЧАСТЬ 2: ФОН (Backend Logic)

### 2.1 Основные компоненты системы

#### Device Manager
Управляет подключением и здоровьем каждого Pixel'я:
- Проверяет онлайн/оффлайн статус каждые 60 сек
- Мониторит батарею, температуру, память, интернет
- Автоматически восстанавливает соединение при разрыве
- Перезагружает девайс при критических ошибках
- Логирует все действия локально

#### Task Orchestrator
Планирует и выполняет сценарии:
- Читает сценарии из UI/БД
- Распределяет задачи между доступными Pixel'ми
- Управляет очередью (priority, scheduling)
- Выполняет каждый шаг сценария последовательно
- Обновляет прогресс в реальном времени

#### AI Agent (DroidRun wrapper)
Взаимодействует с UI приложений на телефонах:
- Получает скриншоты и UI иерархию (XML)
- Находит элементы для клика (selector matching)
- Выполняет действия (tap, swipe, type)
- Анализирует результаты через LLM
- Восстанавливается от ошибок

#### Behavior Layer
Эмулирует человеческое поведение:
- Human Typing: буквы печатаются медленно, с паузами, иногда ошибки
- Human Timing: рандомные интервалы между действиями
- Human Gestures: не ровные свайпы, естественные клики
- Human Schedule: активность по локальному времени, перерывы, выходные

#### Integration Layer
Подключение внешних сервисов:
- Notion API: чтение задач, обновление статусов
- Telegram Bot: отправка уведомлений, получение команд
- Gemini 3 Pro LLM: генерация сообщений, анализ скриншотов
- Local Database (SQLite): кеш, логирование, метрики

### 2.2 Поток данных

```
Пользователь создаёт сценарий в UI
           ↓
Сценарий сохраняется в локальную БД
           ↓
Task Orchestrator видит сценарий
           ↓
Распределяет блоки между доступными Pixel'ями
           ↓
Для каждого блока:
  1. Агент получает скриншот/иерархию UI
  2. LLM анализирует состояние
  3. Агент выполняет действие (через Behavior Layer с паузами)
  4. Проверяет результат
  5. Логирует в локальную БД
  6. Обновляет UI с прогрессом
           ↓
Блок успешен → переход к следующему
Блок неудачен → retry или recovery action
           ↓
После сценария:
  1. Обновить статусы в Notion
  2. Отправить Telegram alert
  3. Обновить метрики в БД
  4. Показать результат в Analytics
```

### 2.3 Обработка ошибок и восстановление

**Уровень 1: Retry (первая попытка)**
- Повторить действие с теми же параметрами
- Если успешно → продолжить
- Максимум 2 раза

**Уровень 2: Alternative Path (альтернативный путь)**
- LLM анализирует скриншот и предлагает другой способ
- Например: "Кнопка не по resource-id, ищем по тексту"
- Максимум 1-2 альтернативы

**Уровень 3: Recovery Action (восстановление)**
- Закрыть приложение и открыть заново
- Очистить кеш приложения
- Если интернет упал → перезагрузить Wi-Fi/данные
- Максимум 1 раз

**Уровень 4: Device Reboot (перезагрузка)**
- Если ничего не помогло → перезагрузить Pixel
- Если после перезагрузки ошибка повторяется → alert в Telegram

**Уровень 5: Manual Intervention (ручное вмешательство)**
- Если все 4 уровня не помогли → Telegram alert с вопросом
- "Do you want to skip this task or retry manually?"

### 2.4 Уведомления в Telegram

Бот отправляет уведомления трёх типов:

**INFO (информационные):**
- ✅ Сценарий начался
- ⏳ Задача в очереди
- 📊 Метрики за день

**WARNING (предупреждения):**
- ⚠️ Account might be flagged (WhatsApp)
- 🔥 Device temperature high
- 📱 Low battery

**ERROR (ошибки):**
- ❌ Critical failure
- 🔴 Device offline for 10+ minutes
- 💥 System crash

Для WARNING и ERROR → кнопки для действий:
- [Retry] [Skip] [Pause] [Manual Check] [View Logs]

### 2.5 Notion Integration (только WhatsApp & SMS)

**Читаемая таблица "WhatsApp_Outreach":**
- Message ID (unique identifier)
- Recipient Name
- Phone Number
- Message Content (text from Perplexity)
- Status (Pending → Sent / Failed_InvalidNumber / Failed_Blocked)
- Device Assignment (Auto / Pixel-TH-1 / Pixel-VN-1 / Pixel-TH-2)
- Scheduled Send Time (или пусто = как можно скорее)
- Priority (1-10)
- Created Date
- Sent Date (заполняется после)
- Attempt Count (сколько попыток)
- Notes (комментарии агента)

**Синхронизация:**
- Каждые 60 сек приложение проверяет Notion на новые Pending задачи
- Берёт топ-10 по приоритету
- После отправки обновляет Status, Sent Date, Notes
- Batch updates: собирает 5-10 изменений, отправляет разом (экономит API)

### 2.6 Поддержка Island (двойной WhatsApp)

**Проблема:** Island не предоставляет API для автоматического переключения.

**Решение:**
- Пользователь может создать два отдельных сценария:
  - "WhatsApp Business Account 1"
  - "WhatsApp Business Account 2"
- Каждый сценарий назначен разному Pixel'ю
- Система управляет ими независимо

Если нужно на ОДНОМ Pixel'е:
- Требуется ручное переключение между аккаунтами (через UI)
- Или использование Termux + ADB для автоматизации (сложнее)

---

## ЧАСТЬ 3: ТЕХНИЧЕСКИЕ ТРЕБОВАНИЯ

### 3.1 Технологический стек

**Backend:**
- Python 3.11+
- FastAPI (веб-сервер)
- SQLAlchemy (ORM для БД)
- AsyncIO (асинхронное выполнение)
- Pydantic (валидация данных)

**Frontend:**
- React 18+ (TypeScript)
- Vite (сборка)
- TailwindCSS или styled-components (стили, но с твоей дизайн-системой)
- Axios/Fetch API (HTTP запросы)
- WebSocket (real-time обновления)

**UI компоненты:**
- Boxicons (https://github.com/atisawd/boxicons)
- Simple Icons (https://github.com/simple-icons/simple-icons) для соц сетей
- Chart.js или Recharts для графиков

**Базы данных:**
- SQLite (локально, MVP)
- PostgreSQL (production, если масштабируется)

**External APIs:**
- Notion API (чтение/обновление задач)
- Telegram Bot API (уведомления)
- Google Gemini 3 Pro (LLM)
- ADB over Tailscale (управление Pixel'ями)
- DroidRun / mobile-use (управление UI Android)

### 3.2 Дизайн-система (твоя V3-DESIGN_SYSTEM.md)

Приложение использует 100% твою дизайн-систему:
- **Color palette:** все цвета из системы
- **Typography:** все font sizes, weights, families
- **Spacing:** все gap, padding, margin значения
- **Border radius:** все radius значения
- **Shadows:** все shadow/elevation значения
- **Icons:** Boxicons + Simple Icons
- **Components:** Button, Card, Modal, Input, Select и т.д. — все по системе

### 3.3 Performance & Optimization

**Скорость:**
- Одно WhatsApp сообщение: 20-45 сек (не 3-6 как обычно в браузере)
- Достигается за счёт минимизации скриншотов (XML parsing вместо анализа изображений)

**Масштабируемость:**
- Может управлять 3-5 Pixel'ми параллельно на одном ПК
- При 10+ Pixel'ях рекомендуется запустить на VPS

**Стабильность:**
- Все данные синхронизируются локально (не зависит от облака)
- Если Notion упадёт → приложение работает с локальной БД
- При восстановлении Notion → автоматическая ресинхронизация

---

## ЧАСТЬ 4: РАЗВЁРТЫВАНИЕ И ЗАПУСК

### 4.1 Начальная настройка Pixel'й

На КАЖДОМ из трёх Pixel'й (делается один раз дома, ДО отправки в Азию):

1. Developer Mode включен (Settings → About phone → tap 7x Build Number)
2. USB Debug ON + Wireless Debug ON
3. Tailscale установлен и авторизован
4. Every Proxy (или аналог) установлен, порт 1080 настроен
5. Проверка через `adb connect pixel-xxx:5555`

### 4.2 Первичный запуск приложения

```bash
# 1. Клон репозитория
git clone <repo_url>
cd android-agent-platform

# 2. Установка Python зависимостей
pip install -r requirements.txt

# 3. Установка Node зависимостей (frontend)
cd frontend
npm install
cd ..

# 4. Создание .env файла
cp config/.env.example .env
# Заполнить: NOTION_KEY, TELEGRAM_TOKEN, GEMINI_KEY

# 5. Инициализация БД
python scripts/init_db.py

# 6. Запуск backend
python -m uvicorn src.main:app --reload

# 7. В другом терминале: frontend
cd frontend
npm run dev

# 8. Открыть http://localhost:3000
```

### 4.3 Первый день использования

- Запустить Dashboard, проверить что все 3 Pixel'я online
- Создать simple сценарий (1-2 WhatsApp сообщения) и запустить как test
- Проверить логи — всё ли корректно работает
- Если OK → начать с полных сценариев

---

## ЧАСТЬ 5: ОГРАНИЧЕНИЯ И ЧЕСТНОСТЬ

### Что работает идеально:
✅ WhatsApp рассылка персонализированных сообщений
✅ LinkedIn лайки и подписки
✅ Instagram Reels постинг
✅ Эмуляция человеческого поведения
✅ Интеграция с Notion
✅ Telegram уведомления
✅ Восстановление от ошибок

### Что имеет лимиты:
⚠️ Instagram комменты (высокий риск блокировки, не рекомендуется)
⚠️ LinkedIn комменты (нужна осторожность, мало текста, высокое качество)
⚠️ Island двойной WhatsApp (требует ручного переключения или сложный Termux скрипт)

### Что может измениться:
🔄 Instagram UI часто обновляется → селекторы могут сломаться
🔄 WhatsApp может обновить дизайн → может потребоваться обновление селекторов

---

## ИТОГОВАЯ КАРТИНА

На выходе ты получаешь:

✅ **Desktop приложение** (Windows/Mac/Linux)
✅ **Полный контроль** над тремя Pixel'ми в Азии
✅ **Красивый интерфейс** согласно твоей дизайн-системе
✅ **Automation** WhatsApp, LinkedIn, Instagram
✅ **Real-time мониторинг** в UI
✅ **Telegram alerts** для важных событий
✅ **Notion интеграция** для управления рассылками
✅ **AI-агент** на основе Gemini 3 Pro
✅ **Production-готовая система** для коммерциализации

Это не просто скрипт — это **профессиональный инструмент**, который работает стабильно 24/7, выглядит профессионально и может быть использован коммерчески или распространяться как open-source.
