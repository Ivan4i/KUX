# Frontend - Детальное описание

## Структура фронтенда

```
frontend/src/
├── main.tsx                 # Точка входа React
├── App.tsx                  # Главный компонент с роутингом
├── index.css                # Глобальные стили
├── components/              # UI компоненты
│   ├── common/              # Общие компоненты
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Input.tsx
│   ├── dashboard/           # Компоненты дашборда
│   │   ├── CurrentActivity.tsx
│   │   ├── DeviceCard.tsx
│   │   └── RecentLogs.tsx
│   └── scenarios/           # Компоненты сценариев
│       ├── ScenarioBuilder.tsx
│       ├── ScenarioCard.tsx
│       ├── StepCard.tsx
│       └── StepEditor.tsx
├── hooks/                   # React хуки
│   └── useWebSocket.ts
├── pages/                   # Страницы приложения
│   ├── AgentsPage.tsx
│   ├── AnalyticsPage.tsx
│   ├── DashboardPage.tsx
│   ├── DevicesPage.tsx
│   ├── LogsPage.tsx
│   ├── ScenariosPage.tsx
│   ├── SettingsPage.tsx
│   └── TasksPage.tsx
├── services/                # Сервисы
│   ├── api.ts
│   └── websocket.ts
└── types/                   # TypeScript типы
    ├── device.ts
    ├── log.ts
    ├── scenario.ts
    ├── task.ts
    └── websocket.ts
```

---

## main.tsx - Точка входа

### Описание
Инициализирует React приложение и подключает React Router.

```tsx
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
)
```

---

## App.tsx - Главный компонент

### Описание
Главный компонент приложения. Содержит:
- Боковую навигацию
- Систему роутинга
- Toast уведомления

### Навигационные элементы
| Иконка | Путь | Страница | Описание |
|--------|------|----------|----------|
| `FaHome` | `/` | DashboardPage | Главная панель |
| `FaMobileAlt` | `/devices` | DevicesPage | Устройства |
| `FaTasks` | `/tasks` | TasksPage | Задачи |
| `FaProjectDiagram` | `/scenarios` | ScenariosPage | Сценарии |
| `FaRobot` | `/agents` | AgentsPage | AI Агенты |
| `FaChartBar` | `/analytics` | AnalyticsPage | Аналитика |
| `FaList` | `/logs` | LogsPage | Логи |
| `FaCog` | `/settings` | SettingsPage | Настройки |

### Структура макета
```
┌────────────────────────────────────────────────────┐
│ Боковая панель (w-64)                              │
│ ┌────────────────────────────────────────────────┐ │
│ │ Лого: KUX + Android Agent Platform            │ │
│ └────────────────────────────────────────────────┘ │
│ ┌────────────────────────────────────────────────┐ │
│ │ Навигация:                                      │ │
│ │ - Dashboard                                     │ │
│ │ - Devices                                       │ │
│ │ - Tasks                                         │ │
│ │ - Scenarios                                     │ │
│ │ - Agents                                        │ │
│ │ - Analytics                                     │ │
│ │ - Logs                                          │ │
│ │ - Settings                                      │ │
│ └────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────┤
│ Основной контент (flex-1)                          │
│ ┌────────────────────────────────────────────────┐ │
│ │ <Routes>                                        │ │
│ │   Контент текущей страницы                     │ │
│ │ </Routes>                                       │ │
│ └────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────┘
```

---

## Страницы (Pages)

### DashboardPage.tsx - Главная панель

#### Описание
Отображает общую статистику платформы.

#### Состояние
| State | Тип | Описание |
|-------|-----|----------|
| `devices` | DeviceStatus[] | Список устройств |
| `tasks` | Task[] | Задачи в статусе Pending |
| `logs` | Log[] | Последние 10 логов |
| `currentTask` | Task \| null | Текущая выполняемая задача |
| `taskProgress` | TaskProgress \| null | Прогресс текущей задачи |
| `isLoading` | boolean | Загрузка данных |
| `isSyncing` | boolean | Синхронизация с Notion |
| `isRunning` | boolean | Выполнение задачи |

#### Функции
| Функция | Описание |
|---------|----------|
| `loadData()` | Загрузка устройств, задач, логов |
| `handleSyncNotion()` | Синхронизация задач из Notion |
| `handleRunTask()` | Запуск следующей задачи |
| `handleRefreshDevices()` | Обновление статуса устройств |

#### UI элементы
- **Заголовок**: "Dashboard" + кнопки "Sync Notion" и "Run Task"
- **Статистика**: 4 карточки (Pending/Running/Devices Online/Success Rate)
- **Сетка 2 колонки**:
  - Левая: Устройства (DeviceCard) + Текущая активность (CurrentActivity)
  - Правая: Последние логи (RecentLogs)

#### WebSocket интеграция
Подписка на события:
- `task_started` → обновление currentTask
- `task_progress` → обновление taskProgress
- `task_completed` → перезагрузка данных
- `task_failed` → перезагрузка данных
- `device_status_update` → обновление устройства

---

### DevicesPage.tsx - Управление устройствами

#### Описание
Детальная информация о всех подключенных устройствах.

#### Состояние
| State | Тип | Описание |
|-------|-----|----------|
| `devices` | DeviceStatus[] | Список устройств |
| `selectedDevice` | string \| null | Выбранное устройство |
| `isLoading` | boolean | Загрузка |
| `isRefreshing` | boolean | Обновление устройства |

#### Функции
| Функция | Описание |
|---------|----------|
| `loadDevices()` | Загрузка списка устройств |
| `handleRefresh(deviceId)` | Обновление статуса устройства |
| `handleReboot(deviceId)` | Перезагрузка устройства |
| `handleScreenshot(deviceId)` | Получение скриншота |
| `handleScrcpy(deviceId)` | Запуск зеркалирования экрана |

#### UI элементы
- **Заголовок**: "Devices" + кнопка "Refresh All"
- **Сетка устройств**: Карточки с информацией
- **Панель деталей**: При выборе устройства
  - Статус, батарея, температура, сигнал
  - Кнопки: Screenshot, Reboot, Screen Mirror

---

### TasksPage.tsx - Управление задачами

#### Описание
Список всех задач с фильтрацией и управлением.

#### Состояние
| State | Тип | Описание |
|-------|-----|----------|
| `tasks` | Task[] | Список задач |
| `filter` | string | Фильтр по статусу |
| `deviceFilter` | string | Фильтр по устройству |
| `isLoading` | boolean | Загрузка |

#### Функции
| Функция | Описание |
|---------|----------|
| `loadTasks()` | Загрузка задач с фильтрами |
| `handleRunTask(taskId)` | Запуск конкретной задачи |
| `handleDeleteTask(taskId)` | Удаление задачи |
| `handleSyncNotion()` | Синхронизация с Notion |

#### Таблица задач
| Колонка | Описание |
|---------|----------|
| ID | Номер задачи |
| Recipient | Имя + номер телефона |
| Message | Превью сообщения |
| Status | Статус с цветным бейджем |
| Device | Назначенное устройство |
| Priority | Приоритет |
| Created | Дата создания |
| Actions | Кнопки действий |

#### Статусы задач
| Статус | Цвет | Описание |
|--------|------|----------|
| `Pending` | yellow | Ожидает выполнения |
| `Running` | blue | Выполняется |
| `Sent` | green | Успешно отправлено |
| `Failed` | red | Ошибка |

---

### ScenariosPage.tsx - Управление сценариями

#### Описание
Список сценариев автоматизации с возможностью редактирования.

#### Состояние
| State | Тип | Описание |
|-------|-----|----------|
| `scenarios` | ScenarioListItem[] | Список сценариев |
| `selectedScenario` | Scenario \| null | Выбранный сценарий |
| `isLoading` | boolean | Загрузка |
| `isEditing` | boolean | Режим редактирования |
| `showCreateModal` | boolean | Модалка создания |

#### Функции
| Функция | Описание |
|---------|----------|
| `loadScenarios()` | Загрузка списка сценариев |
| `handleCreate(data)` | Создание сценария |
| `handleEdit(id)` | Редактирование сценария |
| `handleDelete(id)` | Удаление сценария |
| `handleDuplicate(id)` | Копирование сценария |
| `handleRun(id)` | Запуск сценария |
| `handlePause(id)` | Пауза сценария |
| `handleCancel(id)` | Отмена сценария |

#### Режимы отображения
1. **Список сценариев**: Карточки ScenarioCard
2. **Редактор сценария**: ScenarioBuilder с Drag & Drop

---

### AgentsPage.tsx - Настройка AI агентов

#### Описание
Конфигурация AI агентов и их промптов.

#### Доступные агенты
| Агент | Статус | Иконка | Цвет |
|-------|--------|--------|------|
| WhatsApp | active | FaWhatsapp | green |
| Instagram | coming_soon | FaInstagram | pink |
| LinkedIn | coming_soon | FaLinkedin | blue |
| Telegram | coming_soon | FaTelegram | blue |

#### WhatsApp Agent - Промпты
| Ключ | Название | Описание |
|------|----------|----------|
| `screen_analysis` | Screen Analysis Prompt | Анализ скриншотов WhatsApp |
| `message_personalization` | Message Personalization Prompt | Персонализация сообщений |
| `element_location` | Element Location Prompt | Поиск UI элементов |

#### WhatsApp Agent - Настройки
| Ключ | Тип | По умолчанию | Описание |
|------|-----|--------------|----------|
| `max_retries` | number | 3 | Макс. повторов |
| `typing_speed` | select | normal | Скорость набора |
| `add_typos` | boolean | false | Добавлять опечатки |
| `warmup_enabled` | boolean | true | Включить прогрев |
| `warmup_duration` | number | 60 | Длительность прогрева (сек) |

#### Вкладки
1. **Prompts**: Редактирование промптов + кнопка Test
2. **Settings**: Настройки агента
3. **Available Actions**: Список доступных действий

**ВАЖНО**: Сохранение конфигурации в бэкенд НЕ РЕАЛИЗОВАНО (TODO в коде)

---

### AnalyticsPage.tsx - Аналитика

#### Описание
Статистика и метрики платформы.

#### Состояние
| State | Тип | Описание |
|-------|-----|----------|
| `devices` | DeviceStatus[] | Устройства |
| `tasks` | Task[] | Задачи |
| `timeRangeStats` | TimeRangeStats[] | Статистика по периодам |
| `selectedRange` | number | Выбранный период (часы) |

#### Периоды статистики
| Период | Часы |
|--------|------|
| Last Hour | 1 |
| Last 24 Hours | 24 |
| Last Week | 168 |
| Last Month | 720 |

#### Отображаемые метрики
- **Total Actions**: Всего действий
- **Successful**: Успешных
- **Failed**: Неуспешных
- **Warnings**: Предупреждений

#### Компоненты
1. **SuccessRateGauge**: Круговой индикатор успешности
2. **BarChart**: Гистограмма действий по типу
3. **Tasks Overview**: Распределение задач по статусам
4. **Device Health**: Здоровье устройств

---

### LogsPage.tsx - Логи

#### Описание
Детальный просмотр логов с фильтрацией.

#### Фильтры
| Фильтр | Опции |
|--------|-------|
| Status | all, success, warning, failed |
| Device | Список устройств |
| Time Range | 1h, 24h, 7d, 30d |

#### Функции
| Функция | Описание |
|---------|----------|
| `loadLogs()` | Загрузка логов с фильтрами |
| `handleCleanup(days)` | Очистка старых логов |
| `handleExport()` | Экспорт логов (не реализован) |

#### Таблица логов
| Колонка | Описание |
|---------|----------|
| Time | Время события |
| Device | ID устройства |
| Task | ID задачи (если есть) |
| Action | Тип действия |
| Status | Статус с иконкой |
| Details | Детали события |

---

### SettingsPage.tsx - Настройки

#### Описание
Конфигурация интеграций и поведения системы.

#### Секции настроек

##### 1. Integrations (Интеграции)
| Поле | Тип | Описание |
|------|-----|----------|
| `notion_api_key` | password | API ключ Notion |
| `notion_database_id` | text | ID базы данных Notion |
| `telegram_bot_token` | password | Токен Telegram бота |
| `telegram_chat_id` | text | ID чата Telegram |
| `puter_api_key` | password | API ключ Puter |
| `puter_api_url` | text | URL API Puter |
| `puter_default_model` | text | Модель по умолчанию |

##### 2. Behavior (Поведение)
| Поле | Тип | Диапазон | Описание |
|------|-----|----------|----------|
| `min_typing_delay_ms` | number | 0-1000 | Мин. задержка набора |
| `max_typing_delay_ms` | number | 0-1000 | Макс. задержка набора |
| `min_action_delay_ms` | number | 0-5000 | Мин. задержка действия |
| `max_action_delay_ms` | number | 0-5000 | Макс. задержка действия |
| `typo_probability` | number | 0-1 | Вероятность опечатки |
| `typo_fix_probability` | number | 0-1 | Вероятность исправления |
| `max_messages_per_hour` | number | 1-100 | Макс. сообщений/час |
| `max_messages_per_day` | number | 1-500 | Макс. сообщений/день |
| `cooldown_after_batch_min` | number | 0-120 | Пауза после batch |

##### 3. App Settings (Приложение)
| Поле | Тип | Опции | Описание |
|------|-----|-------|----------|
| `app_env` | select | development, production | Окружение |
| `app_debug` | boolean | - | Режим отладки |
| `log_level` | select | DEBUG, INFO, WARNING, ERROR | Уровень логов |

#### Функции тестирования
| Функция | Описание |
|---------|----------|
| `testNotionConnection()` | Тест подключения к Notion |
| `testTelegramConnection()` | Тест подключения к Telegram |

---

## Компоненты (Components)

### common/Button.tsx

#### Props
| Prop | Тип | По умолчанию | Описание |
|------|-----|--------------|----------|
| `variant` | string | 'primary' | Стиль кнопки |
| `size` | string | 'md' | Размер |
| `isLoading` | boolean | false | Состояние загрузки |
| `leftIcon` | ReactNode | - | Иконка слева |
| `rightIcon` | ReactNode | - | Иконка справа |

#### Варианты
| Variant | Цвета |
|---------|-------|
| `primary` | bg-primary-600, text-white |
| `secondary` | bg-gray-200, text-gray-900 |
| `success` | bg-success-600, text-white |
| `warning` | bg-warning-600, text-white |
| `error` / `danger` | bg-error-600, text-white |
| `ghost` | bg-transparent, text-gray-700 |

### common/Card.tsx

#### Props
| Prop | Тип | Описание |
|------|-----|----------|
| `title` | string | Заголовок |
| `subtitle` | string | Подзаголовок |
| `headerAction` | ReactNode | Действие в заголовке |
| `padding` | 'none'\|'sm'\|'md'\|'lg' | Отступы |

### dashboard/DeviceCard.tsx

#### Описание
Карточка устройства с информацией о статусе.

#### Props
| Prop | Тип | Описание |
|------|-----|----------|
| `device` | DeviceStatus | Данные устройства |

#### Отображает
- Название и локацию
- Статус (online/offline/busy) с цветным индикатором
- Батарею с иконкой (цвет зависит от уровня)
- Температуру (цвет зависит от значения)
- Силу сигнала
- Количество задач за сегодня
- Кнопка "Screen" для запуска scrcpy

### dashboard/CurrentActivity.tsx

#### Описание
Отображение текущей выполняемой задачи.

#### Props
| Prop | Тип | Описание |
|------|-----|----------|
| `task` | Task \| null | Текущая задача |
| `progress` | TaskProgress \| null | Прогресс выполнения |

#### Состояния
1. **Нет задачи**: Заглушка "No active tasks"
2. **Есть задача**: Информация + прогресс-бар

### dashboard/RecentLogs.tsx

#### Описание
Список последних логов.

#### Props
| Prop | Тип | Описание |
|------|-----|----------|
| `logs` | Log[] | Массив логов |

#### Иконки статусов
| Статус | Иконка | Цвет |
|--------|--------|------|
| success | FaCheckCircle | success-500 |
| warning | FaExclamationTriangle | warning-500 |
| failed | FaTimesCircle | error-500 |

### scenarios/ScenarioCard.tsx

#### Описание
Карточка сценария в списке.

#### Props
| Prop | Тип | Описание |
|------|-----|----------|
| `scenario` | ScenarioListItem | Данные сценария |
| `onRun` | (id) => void | Запуск |
| `onPause` | (id) => void | Пауза |
| `onCancel` | (id) => void | Отмена |
| `onEdit` | (id) => void | Редактирование |
| `onDuplicate` | (id) => void | Копирование |
| `onDelete` | (id) => void | Удаление |
| `isLoading` | boolean | Загрузка |

#### Кнопки (зависят от статуса)
- **draft/completed/failed/cancelled**: Run, Edit, Copy, Delete
- **running**: Pause, Cancel
- **paused**: Resume, Cancel

### scenarios/ScenarioBuilder.tsx

#### Описание
Визуальный конструктор сценария с Drag & Drop.

#### Функционал
- Редактирование названия и описания сценария
- Добавление/редактирование/удаление шагов
- Drag & Drop сортировка шагов (@dnd-kit)
- Запуск/пауза/отмена сценария
- Настройка CRON расписания

#### CRON пресеты
| Название | Выражение |
|----------|-----------|
| Every hour | 0 * * * * |
| Daily 9 AM | 0 9 * * * |
| Mon-Fri 9 AM | 0 9 * * 1-5 |
| Weekly Mon | 0 9 * * 1 |

### scenarios/StepEditor.tsx

#### Описание
Модальное окно редактирования шага сценария.

#### Поля
| Поле | Тип | Обязательное |
|------|-----|--------------|
| Step Name | text | Нет |
| Agent | select | Да |
| Action | select | Да |
| Parameters | dynamic | Зависит от action |
| Delay Before | number | Нет |
| Timeout | number | Нет |
| Max Retries | number | Нет |
| Condition | text | Нет |

#### Параметры по action
Определены в `ACTION_PARAMETERS`:
- `whatsapp:send_message`: recipient, message, recipient_name, personalize, use_typos
- `whatsapp:warmup`: duration_seconds
- `whatsapp:send_batch_messages`: recipients (JSON), delay_between
- `whatsapp:check_delivery`: recipient

### scenarios/StepCard.tsx

#### Описание
Карточка шага в конструкторе сценария.

#### Функционал
- Drag handle для сортировки
- Иконка агента с цветной левой границей
- Номер шага
- Название и статус
- Превью параметров
- Кнопки Edit и Delete

---

## Сервисы (Services)

### api.ts - HTTP клиент

#### Базовая конфигурация
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})
```

#### Функции API
Подробное описание в [API.md](./04_API.md)

### websocket.ts - WebSocket клиент

#### Класс `WebSocketService`

##### Атрибуты
```typescript
private ws: WebSocket | null = null
private url: string
private reconnectInterval: number = 5000
private messageHandlers: Set<MessageHandler> = new Set()
private isIntentionallyClosed: boolean = false
```

##### Методы
| Метод | Описание |
|-------|----------|
| `connect()` | Подключение к WebSocket |
| `disconnect()` | Отключение |
| `subscribe(handler)` | Подписка на сообщения |
| `send(message)` | Отправка сообщения |
| `isConnected()` | Проверка подключения |

##### Автоматический реконнект
- При разрыве соединения - повторное подключение через 5 секунд
- Не переподключается если закрыто намеренно (`isIntentionallyClosed`)

---

## Хуки (Hooks)

### useWebSocket.ts

#### `useWebSocket()`
Основной хук для работы с WebSocket.

```typescript
const { subscribe, send, isConnected } = useWebSocket()
```

- Подключается при монтировании
- Отключается при размонтировании

#### `useWebSocketMessages<T>(messageType, handler)`
Специализированный хук для определенного типа сообщений.

```typescript
useWebSocketMessages<TaskProgressMessage>('task_progress', (msg) => {
  setProgress(msg)
})
```

---

## Типы (Types)

### device.ts
```typescript
interface DeviceStatus {
  id: string
  name: string
  location: string
  current_status: 'online' | 'offline' | 'busy'
  battery_level: number
  temperature: number
  signal_strength: number
  last_heartbeat: string | null
  active_task_id: number | null
  tasks_completed_today: number
}
```

### task.ts
```typescript
interface Task {
  id: number
  notion_id: string | null
  recipient_name: string
  phone_number: string
  message_content: string
  status: 'Pending' | 'Running' | 'Sent' | 'Failed'
  device_id: string | null
  device_assignment: string
  priority: number
  created_date: string | null
  scheduled_send_time: string | null
  sent_date: string | null
  attempt_count: number
  notes: string
  created_at: string
  started_at: string | null
  completed_at: string | null
}

interface TaskProgress {
  task_id: number
  message: string
  progress_percent: number | null
}
```

### scenario.ts
```typescript
type ScenarioStatus = 'draft' | 'pending' | 'running' | 'paused' | 'completed' | 'failed' | 'cancelled'
type StepStatus = 'pending' | 'running' | 'completed' | 'failed' | 'skipped'
type AgentType = 'whatsapp' | 'instagram' | 'linkedin' | 'telegram'

interface Scenario {
  id: string
  name: string
  description?: string
  status: ScenarioStatus
  is_template: boolean
  cron_expression?: string
  scheduled_at?: string
  current_step_index: number
  total_steps: number
  started_at?: string
  completed_at?: string
  steps: ScenarioStep[]
  // ...
}

interface ScenarioStep {
  id: string
  scenario_id: string
  order_index: number
  name: string
  agent_type: AgentType
  action: string
  parameters: Record<string, any>
  condition?: string
  delay_before_seconds: number
  timeout_seconds: number
  max_retries: number
  status: StepStatus
  // ...
}
```

### log.ts
```typescript
interface Log {
  id: number
  device_id: string
  task_id: number | null
  action_type: string
  status: 'success' | 'warning' | 'failed'
  details: string
  screenshot_path: string | null
  created_at: string
}

interface LogsSummary {
  time_range_hours: number
  total_logs: number
  success_count: number
  warning_count: number
  failed_count: number
  success_rate: number
  action_counts: Record<string, number>
}
```

### websocket.ts
```typescript
interface WebSocketMessage {
  type: string
  timestamp: string
  [key: string]: any
}

// Типы сообщений:
interface DeviceStatusUpdateMessage extends WebSocketMessage { type: 'device_status_update' }
interface TaskStartedMessage extends WebSocketMessage { type: 'task_started' }
interface TaskProgressMessage extends WebSocketMessage { type: 'task_progress' }
interface TaskCompletedMessage extends WebSocketMessage { type: 'task_completed' }
interface TaskFailedMessage extends WebSocketMessage { type: 'task_failed' }
interface LogEntryMessage extends WebSocketMessage { type: 'log_entry' }
interface NotificationMessage extends WebSocketMessage { type: 'notification' }
```

---

## Конфигурация

### vite.config.ts
```typescript
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': { target: 'http://localhost:8000', changeOrigin: true },
      '/ws': { target: 'ws://localhost:8000', ws: true },
    },
  },
})
```

### tailwind.config.js
Кастомные цвета:
- `primary`: Blue (sky-500 based)
- `success`: Green (green-500 based)
- `warning`: Orange (amber-500 based)
- `error`: Red (red-500 based)

---

## Следующий документ

[API.md](./04_API.md) - Полное описание API эндпоинтов
