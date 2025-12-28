# KUX Project Structure

## Overview

**Project:** Android Agent Platform (KUX)
**Description:** Desktop приложение для автоматизации WhatsApp рассылок через реальные Android устройства (Google Pixel 5), подключенные через VPN (Tailscale) с использованием ADB и AI агентов.

---

## Directory Tree

```
KUX/
│
├── .claude/                           # Конфигурация для Claude AI
│   ├── coding-guidelines.md          # Стандарты кодирования проекта
│   ├── project-prompt.md             # Главный системный промпт (v2.0)
│   ├── promt-dev-base.md             # Базовые принципы разработки
│   └── settings.local.json           # Локальные настройки
│
├── backend/                           # Python FastAPI Backend
│   ├── src/                          # Основной код
│   │   ├── main.py                   # Точка входа приложения
│   │   ├── config.py                 # Конфигурация приложения
│   │   │
│   │   ├── routes/                   # API endpoints
│   │   │   ├── devices.py            # Endpoints для управления устройствами
│   │   │   ├── tasks.py              # Endpoints для задач
│   │   │   ├── scenarios.py          # Endpoints для сценариев
│   │   │   ├── logs.py               # Endpoints для логов
│   │   │   └── settings.py           # Endpoints для настроек
│   │   │
│   │   ├── device_manager/           # Управление Android устройствами
│   │   │   ├── manager.py            # Менеджер устройств
│   │   │   ├── device.py             # Модель устройства
│   │   │   ├── adb_handler.py        # ADB (Android Debug Bridge) handler
│   │   │   ├── health_monitor.py     # Мониторинг здоровья устройства
│   │   │   └── __init__.py
│   │   │
│   │   ├── agents/                   # AI Agents для автоматизации
│   │   │   ├── base_agent.py         # Базовый класс агента
│   │   │   ├── whatsapp_agent.py     # WhatsApp агент
│   │   │   ├── droidrun_wrapper.py   # Обертка для DroidRun
│   │   │   └── __init__.py
│   │   │
│   │   ├── behaviors/                # Эмуляция человеческого поведения
│   │   │   ├── human_gestures.py     # Жесты и прикосновения
│   │   │   ├── human_timing.py       # Временные задержки (реалистичные)
│   │   │   ├── human_typing.py       # Имитация набора текста человеком
│   │   │   └── __init__.py
│   │   │
│   │   ├── orchestration/            # Оркестрация задач и сценариев
│   │   │   ├── queue_manager.py      # Менеджер очереди задач
│   │   │   ├── task_scheduler.py     # Планировщик задач
│   │   │   ├── scenario_runner.py    # Выполняющий сценарии
│   │   │   └── __init__.py
│   │   │
│   │   ├── integrations/             # Интеграции с внешними сервисами
│   │   │   ├── notion_client.py      # Интеграция с Notion
│   │   │   ├── telegram_bot.py       # Telegram уведомления
│   │   │   ├── puter_client.py       # Puter.js API клиент
│   │   │   └── __init__.py
│   │   │
│   │   ├── database/                 # Работа с БД
│   │   │   ├── db.py                 # Подключение и сессия БД
│   │   │   ├── models.py             # SQLAlchemy ORM модели
│   │   │   ├── schemas.py            # Pydantic схемы для API
│   │   │   └── __init__.py
│   │   │
│   │   ├── websocket/                # WebSocket для real-time обновлений
│   │   │   ├── manager.py            # Менеджер WebSocket соединений
│   │   │   ├── endpoint.py           # WebSocket endpoints
│   │   │   └── __init__.py
│   │   │
│   │   ├── middleware/               # Middleware для обработки запросов
│   │   │   ├── error_handler.py      # Обработка ошибок
│   │   │   └── __init__.py
│   │   │
│   │   ├── utils/                    # Утилиты и помощники
│   │   │   ├── logger.py             # Логирование
│   │   │   └── __init__.py
│   │   │
│   │   └── __init__.py
│   │
│   ├── tests/                        # Тестирование
│   │   ├── unit/                     # Модульные тесты
│   │   │   └── test_whatsapp_agent.py
│   │   ├── integration/              # Интеграционные тесты
│   │   │   └── test_api_tasks.py
│   │   ├── e2e/                      # End-to-End тесты
│   │   ├── conftest.py               # Конфигурация pytest
│   │   └── __init__.py
│   │
│   ├── scripts/                      # Утилиты и скрипты
│   │   ├── init_db.py               # Инициализация БД
│   │   └── test_connection.py       # Тест подключения ADB
│   │
│   ├── data/                         # Данные приложения (gitignored)
│   │   └── sqlite.db                # SQLite БД
│   │
│   ├── venv/                         # Virtual Environment (Python)
│   ├── requirements.txt              # Зависимости Python
│   ├── Dockerfile                    # Docker контейнеризация
│   ├── .dockerignore                 # Игнорирование для Docker
│   ├── .env.example                  # Пример переменных окружения
│   ├── .env                          # Переменные окружения (gitignored)
│   ├── pytest.ini                    # Конфигурация pytest
│   └── README.md                     # Документация backend
│
├── frontend/                          # React + TypeScript Frontend
│   ├── src/                          # Исходный код приложения
│   │   ├── main.tsx                  # Точка входа React приложения
│   │   ├── App.tsx                   # Главный компонент приложения
│   │   ├── index.css                 # Глобальные стили
│   │   ├── vite-env.d.ts             # Типы для Vite
│   │   │
│   │   ├── components/               # Переиспользуемые компоненты
│   │   │   ├── common/               # Базовые компоненты
│   │   │   │   ├── Button.tsx        # Кнопка
│   │   │   │   ├── Card.tsx          # Карточка
│   │   │   │   └── Input.tsx         # Поле ввода
│   │   │   │
│   │   │   ├── dashboard/            # Компоненты панели управления
│   │   │   │   ├── DeviceCard.tsx    # Карточка устройства
│   │   │   │   ├── CurrentActivity.tsx # Текущая активность
│   │   │   │   └── RecentLogs.tsx    # Последние логи
│   │   │   │
│   │   │   └── scenarios/            # Компоненты для сценариев
│   │   │       ├── ScenarioBuilder.tsx # Конструктор сценариев
│   │   │       ├── ScenarioCard.tsx   # Карточка сценария
│   │   │       ├── StepCard.tsx       # Карточка шага
│   │   │       └── StepEditor.tsx     # Редактор шага
│   │   │
│   │   ├── pages/                    # Страницы приложения
│   │   │   ├── DashboardPage.tsx     # Главная панель управления
│   │   │   ├── DevicesPage.tsx       # Страница устройств
│   │   │   ├── ScenariosPage.tsx     # Страница сценариев
│   │   │   ├── TasksPage.tsx         # Страница задач
│   │   │   ├── AgentsPage.tsx        # Страница агентов
│   │   │   ├── LogsPage.tsx          # Страница логов
│   │   │   ├── AnalyticsPage.tsx     # Страница аналитики
│   │   │   └── SettingsPage.tsx      # Страница настроек
│   │   │
│   │   ├── services/                 # API клиенты и интеграции
│   │   │   ├── api.ts                # Основной API клиент (Axios)
│   │   │   └── websocket.ts          # WebSocket клиент
│   │   │
│   │   ├── types/                    # TypeScript типы
│   │   │   ├── device.ts             # Типы для устройств
│   │   │   ├── task.ts               # Типы для задач
│   │   │   ├── scenario.ts           # Типы для сценариев
│   │   │   ├── log.ts                # Типы для логов
│   │   │   └── websocket.ts          # Типы для WebSocket
│   │   │
│   │   ├── hooks/                    # React Custom Hooks
│   │   │   └── useWebSocket.ts       # Хук для WebSocket
│   │   │
│   │   ├── styles/                   # Стили и тема
│   │   │
│   │   ├── router/                   # Маршрутизация
│   │   │
│   │   └── utils/                    # Утилиты
│   │
│   ├── public/                       # Статические файлы
│   ├── dist/                         # Собранное приложение (build output)
│   │   └── assets/                   # Оптимизированные ассеты
│   │
│   ├── node_modules/                 # Зависимости npm
│   │
│   ├── package.json                  # Конфигурация npm
│   ├── package-lock.json             # Точные версии зависимостей
│   ├── tsconfig.json                 # Конфигурация TypeScript
│   ├── tsconfig.node.json            # TypeScript для конфига Vite
│   ├── vite.config.ts                # Конфигурация Vite (build tool)
│   ├── tailwind.config.js            # Конфигурация TailwindCSS
│   ├── postcss.config.js             # PostCSS конфигурация
│   ├── eslint.config.js              # Конфигурация ESLint
│   └── Dockerfile                    # Docker контейнеризация
│
├── config/                            # Конфигурационные файлы
│   └── devices.yaml                  # Конфигурация Android устройств (3 Pixel 5)
│
├── docs/                              # Документация
│   ├── architecture/                 # Архитектурная документация
│   │   ├── ARCHITECTURE_V2.md        # Основная архитектура системы
│   │   ├── IDEAL_VISION.md           # Идеальное видение проекта
│   │   ├── IMPLEMENTATION_GUIDE.md   # Руководство по реализации
│   │   ├── V3-DESIGN_SYSTEM.md       # Дизайн-система UI/UX
│   │   └── REMOTE_CONTROL_AND_AUTOMATION.md # Автоматизация Android
│   │
│   ├── planning/                     # Планирование проекта
│   │   ├── ROADMAP.md                # Дорожная карта развития
│   │   └── NEXT_STEPS.md             # Следующие шаги
│   │
│   ├── progress/                     # Отслеживание прогресса
│   │   ├── PROGRESS.md               # Основной прогресс
│   │   ├── READINESS_CHECK.md        # Проверка готовности
│   │   ├── UI_READINESS_CHECK.md     # Готовность фронтенда
│   │   ├── SESSION_2_SUMMARY.md      # Резюме сессии 2
│   │   ├── SESSION_3_SUMMARY.md      # Резюме сессии 3
│   │   └── SESSION_3_AUTONOMOUS_SUMMARY.md # Автономная сессия 3
│   │
│   ├── setup/                        # Руководства по установке
│   │   ├── SETUP_GUIDE.md            # Полное руководство установки
│   │   ├── QUICKSTART.md             # Быстрый старт
│   │   └── DEPLOYMENT.md             # Развертывание
│   │
│   └── transport/                    # Транспортная документация
│       ├── README.md
│       ├── CHANGELOG.md
│       ├── TRANSPORT_INDEX.md
│       │
│       ├── alignui/                  # Дизайн-система AlignUI
│       │   ├── README.md
│       │   ├── docs/
│       │   │   ├── ALIGNUI_COMPONENT_MAP.md
│       │   │   └── DESIGN_SYSTEM_MAP.md
│       │   ├── figma/
│       │   │   └── FIGMA_MCP_PLAYBOOK.md
│       │   ├── templates/             # Готовые шаблоны
│       │   │   ├── marketing-template-master/
│       │   │   ├── template-finance-master/
│       │   │   └── template-hr-master/
│       │   └── tokens/
│       │       └── TOKEN_CONTRACT.md
│       │
│       ├── animation/                # Документация по анимации
│       │   ├── README.md
│       │   └── docs/
│       │       ├── 00-index.md
│       │       ├── 01-foundations.md
│       │       ├── 02-animation-basics.md
│       │       ├── 03-css-transforms-properties.md
│       │       ├── 04-values-types.md
│       │       ├── 05-timing-easing.md
│       │       ├── 06-keyframes-stagger.md
│       │       ├── 07-timeline.md
│       │       ├── 08-advanced-features.md
│       │       ├── 09-svg-text.md
│       │       ├── 10-utilities-engine.md
│       │       ├── ANIMATION_INTEGRATION.md
│       │       ├── ANIMATION_PLAYBOOK_ANIMEJS.md
│       │       ├── MOTION_ANIMEJS.md
│       │       └── README.md
│       │
│       └── mcp/                      # MCP документация
│           ├── README.md
│           └── README_MCP.md
│
├── Premium blocks/                    # Премиум блоки и шаблоны
│   ├── Blocks & Components/          # Переиспользуемые блоки
│   └── Sectoral Template/            # Отраслевые шаблоны
│       ├── marketing-template-master/
│       ├── template-finance-master/
│       └── template-hr-master/
│
├── scripts/                           # Глобальные скрипты утилиты
│
├── docker-compose.yml                 # Конфигурация Docker Compose
├── .env.docker.example                # Пример .env для Docker
├── .gitignore                         # Git исключения
└── README.md                          # Главная документация проекта
```

---

## Tech Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| React 18 | UI Framework |
| TypeScript | Type Safety (strict mode) |
| Vite | Build Tool |
| TailwindCSS | Styling |
| Axios | HTTP Client |
| React Router | Navigation |
| @dnd-kit | Drag-and-Drop |
| React Icons | Icon Library |
| React Hot Toast | Notifications |

### Backend
| Technology | Purpose |
|------------|---------|
| Python 3.11+ | Programming Language |
| FastAPI | Web Framework |
| SQLAlchemy | ORM |
| Pydantic | Data Validation |
| AsyncIO | Async Operations |
| UIAutomator2 + ADB | Android Control |
| Scrcpy | Video Streaming |
| Puter.js | LLM API Integration |
| Loguru | Logging |

### Infrastructure
| Technology | Purpose |
|------------|---------|
| Docker + Docker Compose | Containerization |
| PostgreSQL | Production Database |
| SQLite | Development Database |
| Redis | Caching |
| Tailscale | VPN |
| Notion API | Integration |
| Telegram API | Notifications |

---

## Key Components

### 1. Device Manager (`backend/src/device_manager/`)
Управление Android устройствами через ADB:
- Подключение/отключение устройств
- Мониторинг состояния
- Выполнение команд

### 2. AI Agents (`backend/src/agents/`)
Автоматизация мессенджеров:
- WhatsApp Agent - рассылки сообщений
- Base Agent - базовый класс для всех агентов
- DroidRun Wrapper - интеграция с DroidRun

### 3. Human Behaviors (`backend/src/behaviors/`)
Эмуляция человеческого поведения:
- Реалистичные задержки между действиями
- Имитация набора текста с ошибками
- Естественные жесты и прикосновения

### 4. Orchestration (`backend/src/orchestration/`)
Управление задачами и сценариями:
- Очередь задач
- Планировщик
- Выполнение сценариев

### 5. Scenario Builder (`frontend/src/components/scenarios/`)
Визуальный конструктор сценариев:
- Drag-and-drop интерфейс
- Редактирование шагов
- Предпросмотр сценариев

---

## Device Configuration

Конфигурация устройств в `config/devices.yaml`:

```yaml
devices:
  - id: pixel5-1
    name: "Pixel 5 #1"
    tailscale_ip: "100.x.x.x"
    timezone: "Asia/Bangkok"
    max_tasks_per_day: 100
    active_hours: "09:00-21:00"

  - id: pixel5-2
    name: "Pixel 5 #2"
    ...

  - id: pixel5-3
    name: "Pixel 5 #3"
    ...
```

---

## Current Status

| Aspect | Status |
|--------|--------|
| **Phase** | Slice 1 - MVP WhatsApp Flow |
| **Session** | Season 3 |
| **Progress** | Base functionality implemented |
| **Next Steps** | Testing & refinement |

---

## Quick Start

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m src.main

# Frontend
cd frontend
npm install
npm run dev

# Docker
docker-compose up -d
```

---

## Documentation Links

- [Architecture](docs/architecture/ARCHITECTURE_V2.md)
- [Design System](docs/architecture/V3-DESIGN_SYSTEM.md)
- [Setup Guide](docs/setup/SETUP_GUIDE.md)
- [Roadmap](docs/planning/ROADMAP.md)
- [Progress](docs/progress/PROGRESS.md)
