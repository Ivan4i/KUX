# Backend - Детальное описание

## Структура бэкенда

```
backend/src/
├── main.py              # Точка входа FastAPI
├── config.py            # Конфигурация приложения
├── agents/              # AI агенты
│   ├── __init__.py
│   ├── base_agent.py
│   ├── droidrun_wrapper.py
│   └── whatsapp_agent.py
├── behaviors/           # Имитация человеческого поведения
│   ├── __init__.py
│   ├── human_gestures.py
│   ├── human_timing.py
│   └── human_typing.py
├── database/            # База данных
│   ├── __init__.py
│   ├── db.py
│   ├── models.py
│   └── schemas.py
├── device_manager/      # Управление устройствами
│   ├── __init__.py
│   ├── adb_handler.py
│   ├── device.py
│   ├── health_monitor.py
│   └── manager.py
├── integrations/        # Внешние интеграции
│   ├── __init__.py
│   ├── notion_client.py
│   ├── puter_client.py
│   └── telegram_bot.py
├── middleware/          # Middleware
│   ├── __init__.py
│   └── error_handler.py
├── orchestration/       # Оркестрация
│   ├── __init__.py
│   ├── queue_manager.py
│   ├── scenario_runner.py
│   └── task_scheduler.py
├── routes/              # API роуты
│   ├── __init__.py
│   ├── devices.py
│   ├── logs.py
│   ├── scenarios.py
│   ├── settings.py
│   └── tasks.py
└── websocket/           # WebSocket
    ├── __init__.py
    ├── endpoint.py
    └── manager.py
```

---

## main.py - Точка входа

### Описание
Главный файл приложения FastAPI. Инициализирует приложение, подключает роуты, настраивает CORS, middleware и события жизненного цикла.

### Ключевые функции

#### `lifespan(app)` - Контекстный менеджер жизненного цикла
- **При запуске (startup)**:
  1. Вызывает `init_db()` - инициализация базы данных
  2. Инициализирует `DeviceManager` с конфигурацией устройств
  3. Сохраняет `device_manager` в `app.state`

- **При остановке (shutdown)**:
  1. Вызывает `device_manager.stop()` для graceful shutdown

### Конфигурация CORS
```python
allow_origins=["*"]          # Все домены разрешены
allow_credentials=True
allow_methods=["*"]
allow_headers=["*"]
```

### Подключенные роуты
| Роутер | Префикс | Теги |
|--------|---------|------|
| devices_router | `/api/devices` | devices |
| tasks_router | `/api/tasks` | tasks |
| logs_router | `/api/logs` | logs |
| scenarios_router | `/api/scenarios` | scenarios |
| settings_router | `/api/settings` | settings |

### Эндпоинты в main.py
| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/` | Возвращает "Hello from KUX API" |
| GET | `/api/health` | Health check - возвращает статус "healthy", версию, timestamp |

### WebSocket
- Путь: `/ws`
- Обработчик: `websocket_endpoint`

---

## config.py - Конфигурация

### Класс `Settings` (extends BaseSettings)
Управляет всеми настройками приложения через переменные окружения.

### Секции настроек

#### App Settings
| Переменная | Тип | По умолчанию | Описание |
|------------|-----|--------------|----------|
| `APP_ENV` | str | "development" | Окружение |
| `APP_DEBUG` | bool | True | Режим отладки |
| `LOG_LEVEL` | str | "DEBUG" | Уровень логирования |

#### Database
| Переменная | Тип | По умолчанию | Описание |
|------------|-----|--------------|----------|
| `DATABASE_URL` | str | "sqlite+aiosqlite:///./kux.db" | URL базы данных |

#### Notion Integration
| Переменная | Тип | По умолчанию | Описание |
|------------|-----|--------------|----------|
| `NOTION_API_KEY` | str \| None | None | API ключ Notion |
| `NOTION_DATABASE_ID` | str \| None | None | ID базы данных Notion |

#### Telegram Integration
| Переменная | Тип | По умолчанию | Описание |
|------------|-----|--------------|----------|
| `TELEGRAM_BOT_TOKEN` | str \| None | None | Токен Telegram бота |
| `TELEGRAM_CHAT_ID` | str \| None | None | ID чата для уведомлений |

#### Puter LLM Integration
| Переменная | Тип | По умолчанию | Описание |
|------------|-----|--------------|----------|
| `PUTER_API_KEY` | str \| None | None | API ключ Puter |
| `PUTER_API_URL` | str | "https://api.puter.ai/v1" | URL API Puter |
| `PUTER_DEFAULT_MODEL` | str | "claude-sonnet-4.5" | Модель по умолчанию |

#### Human Behavior Settings
| Переменная | Тип | По умолчанию | Описание |
|------------|-----|--------------|----------|
| `MIN_TYPING_DELAY_MS` | int | 50 | Мин. задержка набора (мс) |
| `MAX_TYPING_DELAY_MS` | int | 150 | Макс. задержка набора (мс) |
| `MIN_ACTION_DELAY_MS` | int | 500 | Мин. задержка действия (мс) |
| `MAX_ACTION_DELAY_MS` | int | 2000 | Макс. задержка действия (мс) |
| `TYPO_PROBABILITY` | float | 0.03 | Вероятность опечатки |
| `TYPO_FIX_PROBABILITY` | float | 0.8 | Вероятность исправления |

#### Rate Limiting
| Переменная | Тип | По умолчанию | Описание |
|------------|-----|--------------|----------|
| `MAX_MESSAGES_PER_HOUR` | int | 20 | Макс. сообщений в час |
| `MAX_MESSAGES_PER_DAY` | int | 100 | Макс. сообщений в день |
| `COOLDOWN_AFTER_BATCH_MIN` | int | 30 | Пауза после batch (мин) |

#### Конфигурация устройств (DEVICES_CONFIG)
```python
{
    "phone_1": {
        "name": "Device 1",
        "location": "Bangkok",
        "timezone": "Asia/Bangkok",
        "tailscale_ip": "100.100.100.101",
        "adb_port": 5555,
        "active_hours": "09:00-22:00",
        "max_tasks_per_day": 50
    }
}
```

---

## database/ - Модуль базы данных

### db.py - Подключение к БД

#### Объекты
- `engine` - AsyncEngine SQLAlchemy
- `AsyncSessionLocal` - фабрика асинхронных сессий
- `Base` - декларативная база для моделей

#### Функции
| Функция | Описание |
|---------|----------|
| `get_db()` | Асинхронный генератор сессии БД |
| `init_db()` | Создание всех таблиц при запуске |

### models.py - Модели БД

#### Device (устройство)
| Колонка | Тип | Описание |
|---------|-----|----------|
| `id` | String(50), PK | Уникальный ID устройства |
| `name` | String(100) | Название |
| `location` | String(100) | Локация |
| `timezone` | String(50) | Часовой пояс |
| `tailscale_ip` | String(50) | IP Tailscale |
| `adb_port` | Integer | Порт ADB (default: 5555) |
| `active_hours` | String(50) | Активные часы |
| `max_tasks_per_day` | Integer | Макс. задач в день |
| `current_status` | Enum | online/offline/busy |
| `battery_level` | Integer | Уровень батареи |
| `temperature` | Float | Температура |
| `signal_strength` | Integer | Сила сигнала |
| `last_heartbeat` | DateTime | Последний heartbeat |
| `active_task_id` | Integer | Текущая задача |
| `tasks_completed_today` | Integer | Выполнено задач сегодня |
| `created_at` | DateTime | Дата создания |
| `updated_at` | DateTime | Дата обновления |

#### Task (задача)
| Колонка | Тип | Описание |
|---------|-----|----------|
| `id` | Integer, PK, autoincrement | ID задачи |
| `notion_id` | String(50) | ID в Notion |
| `recipient_name` | String(200) | Имя получателя |
| `phone_number` | String(50), NOT NULL | Номер телефона |
| `message_content` | Text, NOT NULL | Текст сообщения |
| `status` | Enum | Pending/Running/Sent/Failed |
| `device_id` | String(50), FK | ID устройства |
| `device_assignment` | Enum | Auto/Phone_1/Phone_2 |
| `priority` | Integer | Приоритет (default: 0) |
| `created_date` | Date | Дата создания в Notion |
| `scheduled_send_time` | DateTime | Запланированное время |
| `sent_date` | DateTime | Дата отправки |
| `attempt_count` | Integer | Количество попыток |
| `notes` | Text | Заметки |
| `created_at` | DateTime | Дата создания |
| `started_at` | DateTime | Дата начала |
| `completed_at` | DateTime | Дата завершения |

#### Log (лог)
| Колонка | Тип | Описание |
|---------|-----|----------|
| `id` | Integer, PK | ID лога |
| `device_id` | String(50), NOT NULL | ID устройства |
| `task_id` | Integer, FK | ID задачи |
| `action_type` | String(100), NOT NULL | Тип действия |
| `status` | Enum | success/warning/failed |
| `details` | Text | Детали |
| `screenshot_path` | String(500) | Путь к скриншоту |
| `created_at` | DateTime | Время создания |

#### Scenario (сценарий)
| Колонка | Тип | Описание |
|---------|-----|----------|
| `id` | String(36), PK | UUID сценария |
| `name` | String(200), NOT NULL | Название |
| `description` | Text | Описание |
| `status` | Enum | draft/pending/running/paused/completed/failed/cancelled |
| `is_template` | Boolean | Шаблон? |
| `cron_expression` | String(100) | CRON расписание |
| `scheduled_at` | DateTime | Запланированное время |
| `current_step_index` | Integer | Текущий шаг |
| `started_at` | DateTime | Дата начала |
| `completed_at` | DateTime | Дата завершения |
| `result` | JSON | Результат выполнения |
| `error_message` | Text | Сообщение об ошибке |
| `created_by` | String(100) | Создатель |
| `created_at` | DateTime | Дата создания |
| `updated_at` | DateTime | Дата обновления |

#### ScenarioStep (шаг сценария)
| Колонка | Тип | Описание |
|---------|-----|----------|
| `id` | String(36), PK | UUID шага |
| `scenario_id` | String(36), FK | ID сценария |
| `order_index` | Integer | Порядковый номер |
| `name` | String(200) | Название |
| `agent_type` | Enum | whatsapp/instagram/linkedin/telegram |
| `action` | String(100) | Действие |
| `parameters` | JSON | Параметры |
| `condition` | String(500) | Условие выполнения |
| `delay_before_seconds` | Integer | Задержка перед (сек) |
| `timeout_seconds` | Integer | Таймаут (сек) |
| `max_retries` | Integer | Макс. повторов |
| `status` | Enum | pending/running/completed/failed/skipped |
| `result` | JSON | Результат |
| `error_message` | Text | Ошибка |
| `started_at` | DateTime | Начало |
| `completed_at` | DateTime | Завершение |
| `created_at` | DateTime | Создание |

### schemas.py - Pydantic схемы

Содержит схемы для:
- `DeviceStatus` / `DeviceCreate` / `DeviceUpdate`
- `TaskCreate` / `TaskUpdate` / `TaskResponse`
- `LogCreate` / `LogResponse` / `LogSummary`
- `ScenarioCreate` / `ScenarioUpdate` / `ScenarioResponse`
- `ScenarioStepCreate` / `ScenarioStepUpdate` / `ScenarioStepResponse`

---

## agents/ - AI агенты

### base_agent.py - Базовый класс агента

#### Класс `BaseAgent` (ABC)
```python
class BaseAgent(ABC):
    def __init__(self, device: Device, settings: Settings):
        self.device = device
        self.settings = settings
        self.logger = loguru.logger
        self._puter_client: PuterClient | None = None
```

#### Абстрактные методы
| Метод | Описание |
|-------|----------|
| `execute_action(action, params)` | Выполнить действие |
| `warmup()` | Прогрев перед основными действиями |

#### Реализованные методы
| Метод | Описание |
|-------|----------|
| `get_puter_client()` | Получить клиент Puter LLM |
| `personalize_message(template, recipient, context)` | Персонализировать сообщение через AI |

### whatsapp_agent.py - WhatsApp агент

#### Класс `WhatsAppAgent` (extends BaseAgent)

##### Константы
```python
WHATSAPP_PACKAGE = "com.whatsapp"
WAIT_TIMEOUT = 30  # секунд
```

##### Конструктор
```python
def __init__(self, device: Device, settings: Settings):
    self.human_typing = HumanTyping(settings)
    self.human_timing = HumanTiming(settings)
    self.human_gestures = HumanGestures(settings)
```

##### Методы

| Метод | Описание | Статус |
|-------|----------|--------|
| `execute_action(action, params)` | Диспетчер действий | Работает |
| `warmup()` | Прогрев: открывает WhatsApp, скроллит чаты | Работает |
| `send_message(recipient, message, ...)` | Отправка сообщения | Работает |
| `_open_whatsapp()` | Открыть приложение WhatsApp | Работает |
| `_search_contact(phone_number)` | Поиск контакта по номеру | Работает |
| `_type_message(message, use_typos)` | Набор сообщения с имитацией | Работает |
| `_click_send_button()` | Нажатие кнопки отправки | Работает |
| `_wait_for_element(selector, timeout)` | Ожидание UI элемента | Работает |
| `_click_element(element)` | Клик по элементу | Работает |

##### Логика отправки сообщения (`send_message`)
1. Открывает WhatsApp
2. Ждет случайную паузу (human timing)
3. Переходит в поиск (кнопка "New chat")
4. Вводит номер телефона
5. Выбирает контакт или начинает новый чат
6. Вводит сообщение с имитацией набора
7. Если `personalize=True`, персонализирует через AI
8. Если `use_typos=True`, добавляет опечатки
9. Нажимает кнопку отправки
10. Возвращает результат

### droidrun_wrapper.py - Обертка DroidRun

**Статус: Заготовка, не используется**

Класс `DroidRunWrapper` - заготовка для интеграции с DroidRun framework.
Все методы возвращают заглушки `# TODO: implement`.

---

## behaviors/ - Имитация человеческого поведения

### human_typing.py - Имитация набора текста

#### Класс `HumanTyping`

##### Атрибуты
```python
self.settings = settings
self.keyboard_layout = {...}  # QWERTY раскладка
```

##### Методы
| Метод | Описание |
|-------|----------|
| `get_typing_delay()` | Случайная задержка между символами |
| `get_typo_probability()` | Вероятность опечатки |
| `should_make_typo()` | Нужно ли сделать опечатку? |
| `should_fix_typo()` | Нужно ли исправить опечатку? |
| `get_nearby_key(char)` | Получить соседнюю клавишу (для опечатки) |
| `generate_text_with_typos(text)` | Сгенерировать текст с опечатками и исправлениями |

##### Логика опечаток
```python
# Структура результата
[
    {"action": "type", "char": "H", "delay": 75},
    {"action": "type", "char": "e", "delay": 82},
    {"action": "typo", "typed": "l", "intended": "l", "delay": 95},
    {"action": "backspace", "delay": 120},
    {"action": "type", "char": "l", "delay": 90},
    ...
]
```

### human_timing.py - Имитация пауз

#### Класс `HumanTiming`

##### Методы
| Метод | Описание |
|-------|----------|
| `get_action_delay()` | Пауза между действиями (500-2000 мс) |
| `get_reading_delay(text_length)` | Пауза на "чтение" текста |
| `get_thinking_delay()` | Пауза на "обдумывание" (1-3 сек) |
| `get_scroll_pause()` | Пауза после скролла (200-500 мс) |

### human_gestures.py - Имитация жестов

#### Класс `HumanGestures`

##### Методы
| Метод | Описание |
|-------|----------|
| `get_tap_offset()` | Смещение точки касания (±5px) |
| `get_swipe_params()` | Параметры свайпа (duration, steps) |
| `get_drag_params()` | Параметры перетаскивания |
| `calculate_bezier_points(start, end, steps)` | Кривая Безье для естественного движения |

---

## device_manager/ - Управление устройствами

### adb_handler.py - ADB обработчик

#### Класс `ADBHandler`

##### Атрибуты
```python
self.device_id: str          # ID устройства
self.adb_client: AdbClient   # pure-python-adb клиент
self.u2_device: U2Device     # uiautomator2 устройство
```

##### Методы
| Метод | Описание | Возвращает |
|-------|----------|------------|
| `connect(host, port)` | Подключение к устройству | bool |
| `disconnect()` | Отключение | None |
| `is_connected()` | Проверка подключения | bool |
| `get_device_info()` | Информация об устройстве | dict |
| `get_battery_info()` | Информация о батарее | dict |
| `execute_shell(command)` | Выполнить shell команду | str |
| `take_screenshot()` | Сделать скриншот | bytes |
| `start_app(package)` | Запустить приложение | bool |
| `stop_app(package)` | Остановить приложение | bool |
| `tap(x, y)` | Касание экрана | bool |
| `swipe(x1, y1, x2, y2, duration)` | Свайп | bool |
| `input_text(text)` | Ввод текста | bool |
| `reboot()` | Перезагрузка устройства | bool |

### device.py - Класс устройства

#### Класс `Device`

##### Атрибуты
```python
self.id: str
self.config: dict
self.adb: ADBHandler
self.status: DeviceStatus = "offline"
self.battery_level: int = 0
self.temperature: float = 0.0
self.signal_strength: int = 0
```

##### Методы
| Метод | Описание |
|-------|----------|
| `connect()` | Подключиться к устройству |
| `disconnect()` | Отключиться |
| `refresh_status()` | Обновить статус |
| `is_available()` | Доступно ли для задач? |
| `execute_task(task)` | Выполнить задачу |
| `take_screenshot()` | Сделать скриншот |
| `reboot()` | Перезагрузить |

### health_monitor.py - Мониторинг здоровья

#### Класс `HealthMonitor`

##### Атрибуты
```python
self.check_interval: int = 60  # секунды
self.devices: dict[str, Device]
self._running: bool = False
self._task: asyncio.Task | None
```

##### Методы
| Метод | Описание |
|-------|----------|
| `start()` | Запуск мониторинга |
| `stop()` | Остановка мониторинга |
| `_monitor_loop()` | Цикл проверки устройств |
| `check_device(device)` | Проверка одного устройства |
| `get_all_statuses()` | Получить статусы всех устройств |

### manager.py - Менеджер устройств

#### Класс `DeviceManager`

##### Атрибуты
```python
self.devices: dict[str, Device] = {}
self.health_monitor: HealthMonitor
self.settings: Settings
```

##### Методы
| Метод | Описание |
|-------|----------|
| `start()` | Инициализация и запуск |
| `stop()` | Остановка и очистка |
| `get_device(device_id)` | Получить устройство по ID |
| `get_all_devices()` | Получить все устройства |
| `get_available_device()` | Получить свободное устройство |
| `refresh_device(device_id)` | Обновить статус устройства |
| `assign_task(task)` | Назначить задачу на устройство |

---

## integrations/ - Интеграции

### notion_client.py - Клиент Notion

#### Класс `NotionClient`

##### Конструктор
```python
def __init__(self, api_key: str, database_id: str):
    self.client = Client(auth=api_key)
    self.database_id = database_id
```

##### Методы
| Метод | Описание |
|-------|----------|
| `test_connection()` | Тест подключения |
| `get_tasks(limit=10)` | Получить задачи из Notion |
| `update_task_status(page_id, status)` | Обновить статус задачи |
| `_parse_page_to_task(page)` | Парсинг страницы Notion в Task |

##### Ожидаемые поля в Notion базе
| Поле Notion | Тип | Маппинг |
|-------------|-----|---------|
| Name | title | recipient_name |
| Phone Number | rich_text | phone_number |
| Message | rich_text | message_content |
| Status | select | status |
| Device Assignment | select | device_assignment |
| Priority | number | priority |
| Created Date | date | created_date |
| Scheduled Send Time | date | scheduled_send_time |
| Notes | rich_text | notes |

### telegram_bot.py - Telegram бот

#### Класс `TelegramNotifier`

##### Конструктор
```python
def __init__(self, bot_token: str, chat_id: str):
    self.bot = telegram.Bot(token=bot_token)
    self.chat_id = chat_id
```

##### Методы
| Метод | Описание |
|-------|----------|
| `test_connection()` | Отправка тестового сообщения |
| `send_notification(message)` | Отправка уведомления |
| `notify_task_started(task)` | Уведомление о начале задачи |
| `notify_task_completed(task)` | Уведомление о завершении |
| `notify_task_failed(task, error)` | Уведомление об ошибке |
| `notify_device_status(device, status)` | Уведомление о статусе устройства |

### puter_client.py - Клиент Puter LLM

#### Класс `PuterClient`

##### Конструктор
```python
def __init__(self, api_key: str, base_url: str, default_model: str):
    self.api_key = api_key
    self.base_url = base_url
    self.default_model = default_model
    self.http_client = httpx.AsyncClient()
```

##### Методы
| Метод | Описание |
|-------|----------|
| `chat_completion(messages, model=None)` | Запрос к LLM |
| `personalize_message(template, context)` | Персонализация сообщения |
| `analyze_screen(screenshot_base64)` | Анализ скриншота |
| `extract_ui_elements(screenshot_base64)` | Извлечение UI элементов |

---

## orchestration/ - Оркестрация

### task_scheduler.py - Планировщик задач

#### Класс `TaskScheduler`

##### Атрибуты
```python
self.jobs: dict[str, ScheduledJob] = {}
self.running: bool = False
```

##### Методы
| Метод | Описание |
|-------|----------|
| `start()` | Запуск планировщика |
| `stop()` | Остановка планировщика |
| `schedule_scenario(scenario_id, cron)` | Добавить сценарий в расписание |
| `unschedule_scenario(scenario_id)` | Удалить из расписания |
| `get_next_run(scenario_id)` | Получить время следующего запуска |
| `get_all_jobs()` | Получить все запланированные задачи |

### scenario_runner.py - Выполнение сценариев

#### Класс `ScenarioRunner`

##### Атрибуты
```python
self.device_manager: DeviceManager
self.running_scenarios: dict[str, asyncio.Task] = {}
self.paused_scenarios: set[str] = set()
```

##### Методы
| Метод | Описание |
|-------|----------|
| `run_scenario(scenario_id, device_id=None)` | Запуск сценария |
| `pause_scenario(scenario_id)` | Пауза сценария |
| `resume_scenario(scenario_id)` | Продолжение сценария |
| `cancel_scenario(scenario_id)` | Отмена сценария |
| `_execute_step(step, device)` | Выполнение шага |
| `_evaluate_condition(condition, context)` | Проверка условия |
| `_get_agent_for_step(step, device)` | Получить агента для шага |

### queue_manager.py - Менеджер очереди

#### Класс `QueueManager`

##### Атрибуты
```python
self.queue: asyncio.PriorityQueue
self.processing: dict[str, QueueItem] = {}
self.max_concurrent: int = 3
```

##### Методы
| Метод | Описание |
|-------|----------|
| `start()` | Запуск обработки очереди |
| `stop()` | Остановка обработки |
| `add_item(item)` | Добавить элемент в очередь |
| `get_status()` | Получить статус очереди |
| `_process_queue()` | Обработчик очереди |

---

## websocket/ - WebSocket

### manager.py - Менеджер WebSocket

#### Класс `ConnectionManager`

##### Атрибуты
```python
self.active_connections: list[WebSocket] = []
```

##### Методы
| Метод | Описание |
|-------|----------|
| `connect(websocket)` | Подключить клиента |
| `disconnect(websocket)` | Отключить клиента |
| `broadcast(message)` | Отправить всем клиентам |
| `send_personal(websocket, message)` | Отправить конкретному клиенту |

### endpoint.py - WebSocket эндпоинт

#### Функции
| Функция | Описание |
|---------|----------|
| `websocket_endpoint(websocket)` | Обработчик WebSocket соединений |
| `broadcast_device_update(device_id, data)` | Отправка обновления устройства |
| `broadcast_task_update(task_id, data)` | Отправка обновления задачи |
| `broadcast_log_entry(log)` | Отправка нового лога |

#### Типы сообщений
| type | Описание |
|------|----------|
| `device_status_update` | Обновление статуса устройства |
| `task_started` | Задача начата |
| `task_progress` | Прогресс задачи |
| `task_completed` | Задача завершена |
| `task_failed` | Задача провалена |
| `log_entry` | Новая запись в логе |
| `notification` | Уведомление |

---

## middleware/ - Middleware

### error_handler.py - Обработка ошибок

#### Middleware функции
| Функция | Описание |
|---------|----------|
| `exception_handler(request, exc)` | Глобальный обработчик исключений |
| `http_exception_handler(request, exc)` | Обработчик HTTP исключений |
| `validation_exception_handler(request, exc)` | Обработчик ошибок валидации |

#### Формат ответа ошибки
```json
{
    "detail": "Error message",
    "error_code": "ERROR_CODE",
    "timestamp": "2024-01-01T00:00:00Z"
}
```

---

## Следующий документ

[FRONTEND.md](./03_FRONTEND.md) - Детальное описание фронтенда
