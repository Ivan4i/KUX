# KUX - Android Agent Platform

## Общее описание проекта

**KUX** - это платформа для автоматизации мобильных устройств Android с акцентом на отправку сообщений через WhatsApp с имитацией человеческого поведения.

---

## Архитектура проекта

```
KUX/
├── backend/                 # Python FastAPI бэкенд
│   ├── src/
│   │   ├── agents/          # AI агенты для автоматизации
│   │   ├── behaviors/       # Имитация человеческого поведения
│   │   ├── database/        # Модели БД и схемы
│   │   ├── device_manager/  # Управление Android устройствами
│   │   ├── integrations/    # Внешние интеграции (Notion, Telegram, Puter)
│   │   ├── middleware/      # Обработка ошибок
│   │   ├── orchestration/   # Оркестрация сценариев и очередей
│   │   ├── routes/          # API эндпоинты
│   │   ├── websocket/       # WebSocket для реального времени
│   │   ├── config.py        # Конфигурация приложения
│   │   └── main.py          # Точка входа FastAPI
│   ├── scripts/             # Скрипты инициализации
│   ├── tests/               # Тесты
│   └── requirements.txt     # Python зависимости
│
├── frontend/                # React/TypeScript фронтенд
│   ├── src/
│   │   ├── components/      # UI компоненты
│   │   ├── hooks/           # React хуки
│   │   ├── pages/           # Страницы приложения
│   │   ├── services/        # API сервисы
│   │   ├── types/           # TypeScript типы
│   │   ├── App.tsx          # Главный компонент
│   │   └── main.tsx         # Точка входа React
│   ├── package.json         # npm зависимости
│   ├── vite.config.ts       # Конфигурация Vite
│   └── tailwind.config.js   # Конфигурация Tailwind CSS
│
└── .export/                 # Документация проекта
```

---

## Технологический стек

### Backend
| Технология | Версия | Назначение |
|------------|--------|------------|
| **Python** | 3.10+ | Язык программирования |
| **FastAPI** | 0.109.0 | Web-фреймворк |
| **SQLAlchemy** | 2.0.25 | ORM для базы данных |
| **SQLite** | - | База данных (aiosqlite) |
| **Uvicorn** | 0.27.0 | ASGI сервер |
| **Pydantic** | 2.5.3 | Валидация данных |
| **pure-python-adb** | 0.3.0 | ADB для управления Android |
| **uiautomator2** | 3.5.0 | UI автоматизация Android |
| **notion-client** | 2.2.1 | Интеграция с Notion |
| **python-telegram-bot** | 20.7 | Telegram бот |
| **OpenAI** | 1.10.0 | AI/LLM интеграция |
| **Loguru** | 0.7.2 | Логирование |
| **croniter** | 2.0.1 | Парсинг CRON выражений |

### Frontend
| Технология | Версия | Назначение |
|------------|--------|------------|
| **React** | 18.2.0 | UI библиотека |
| **TypeScript** | 5.2.2 | Типизация JavaScript |
| **Vite** | 5.0.8 | Сборщик |
| **Tailwind CSS** | 3.4.0 | CSS фреймворк |
| **React Router** | 6.21.0 | Роутинг |
| **Axios** | 1.6.2 | HTTP клиент |
| **Zustand** | 4.4.7 | State management |
| **@dnd-kit** | 6.1.0+ | Drag & Drop |
| **react-hot-toast** | 2.6.0 | Уведомления |
| **react-icons** | 5.0.1 | Иконки |
| **date-fns** | 3.0.6 | Работа с датами |

---

## Основные функции платформы

### 1. Управление устройствами
- Подключение Android устройств через ADB/Tailscale
- Мониторинг статуса устройств (online/offline/busy)
- Отслеживание батареи, температуры, сигнала
- Скриншоты и зеркалирование экрана через scrcpy
- Перезагрузка устройств

### 2. Управление задачами (Tasks)
- Синхронизация задач из Notion
- Отправка WhatsApp сообщений
- Приоритезация задач
- Отслеживание статуса (Pending/Running/Sent/Failed)
- WebSocket обновления в реальном времени

### 3. Сценарии (Scenarios)
- Визуальный конструктор сценариев
- Drag & Drop сортировка шагов
- Планирование по CRON расписанию
- Поддержка условий выполнения
- Пауза/возобновление/отмена

### 4. AI Агенты
- WhatsApp агент (активен)
- Instagram агент (планируется)
- LinkedIn агент (планируется)
- Telegram агент (планируется)

### 5. Имитация человеческого поведения
- Реалистичные задержки набора текста
- Имитация опечаток с исправлениями
- Естественные жесты (свайпы, касания)
- Ограничения на количество сообщений

### 6. Интеграции
- **Notion**: Синхронизация задач из базы данных
- **Telegram**: Уведомления о статусе задач
- **Puter.js LLM**: Персонализация сообщений через AI

### 7. Логирование и аналитика
- Детальные логи всех действий
- Фильтрация по устройству/статусу/времени
- Статистика успешности
- Очистка старых логов

---

## Порты и URL

| Сервис | Порт | URL |
|--------|------|-----|
| Backend API | 8000 | http://localhost:8000 |
| Frontend Dev | 3000 | http://localhost:3000 |
| WebSocket | 8000 | ws://localhost:8000/ws |
| API Docs | 8000 | http://localhost:8000/docs |

---

## Переменные окружения (.env)

```env
# Приложение
APP_ENV=development
APP_DEBUG=true
LOG_LEVEL=DEBUG

# База данных
DATABASE_URL=sqlite+aiosqlite:///./kux.db

# Notion
NOTION_API_KEY=secret_xxx
NOTION_DATABASE_ID=xxx-xxx-xxx

# Telegram
TELEGRAM_BOT_TOKEN=123456789:ABC...
TELEGRAM_CHAT_ID=-1001234567890

# Puter.js LLM
PUTER_API_KEY=pk_xxx
PUTER_API_URL=https://api.puter.ai/v1
PUTER_DEFAULT_MODEL=claude-sonnet-4.5

# Поведение
MIN_TYPING_DELAY_MS=50
MAX_TYPING_DELAY_MS=150
MIN_ACTION_DELAY_MS=500
MAX_ACTION_DELAY_MS=2000
TYPO_PROBABILITY=0.03
TYPO_FIX_PROBABILITY=0.8
MAX_MESSAGES_PER_HOUR=20
MAX_MESSAGES_PER_DAY=100
COOLDOWN_AFTER_BATCH_MIN=30
```

---

## Запуск проекта

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt
python -m uvicorn src.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## Следующие документы

1. [BACKEND.md](./02_BACKEND.md) - Детальное описание бэкенда
2. [FRONTEND.md](./03_FRONTEND.md) - Детальное описание фронтенда
3. [API.md](./04_API.md) - Полное описание API эндпоинтов
4. [FUNCTIONALITY.md](./05_FUNCTIONALITY.md) - Статус функциональности (что работает/не работает)
