# 💻 TECH STACK: Complete Technology List

## Frontend Stack

### Core Framework & Build

| Technology | Version | Purpose | Why This Choice |
|-----------|---------|---------|-----------------|
| **React** | 18.x | UI library | Modern, component-based, great ecosystem |
| **Vite** | 5.x | Build tool | Fast dev server, optimized production builds |
| **TypeScript** | 5.x | Type safety | Catches errors at compile time, excellent DX |
| **Node.js** | 20 LTS | Runtime | Stable, widely supported |

### UI & Design

| Technology | Version | Purpose | Why This Choice |
|-----------|---------|---------|-----------------|
| **AlignUI** | Latest | Component library | Premium design system, production-ready |
| **CSS Modules** | - | Component styling | Scoped styles, no conflicts |
| **Tailwind CSS** | 3.x | Utility classes | Fast styling, responsive design |
| **anime.js** | 3.x | Animations | Smooth transitions, lightweight |

### State Management & Data

| Technology | Version | Purpose | Why This Choice |
|-----------|---------|---------|-----------------|
| **Zustand** | 4.x | Global state | Lightweight, intuitive API, no boilerplate |
| **Axios** | 1.x | HTTP client | Promise-based, interceptor support |
| **React Query** | 5.x | Server state | Caching, background sync, offline support |
| **WebSocket** | Native | Realtime updates | Built-in browser API, no library needed |

### Development Tools

| Technology | Version | Purpose | Why This Choice |
|-----------|---------|---------|-----------------|
| **ESLint** | 8.x | Code linting | Enforce code quality standards |
| **Prettier** | 3.x | Code formatting | Consistent code style |
| **Jest** | 29.x | Unit testing | Fast, snapshot testing |
| **React Testing Library** | 14.x | Component testing | Best practices for testing React |

---

## Backend Stack

### Core Framework & Runtime

| Technology | Version | Purpose | Why This Choice |
|-----------|---------|---------|-----------------|
| **Python** | 3.11+ | Language | Fast development, rich ecosystem |
| **FastAPI** | 0.104+ | Web framework | Async native, automatic API docs, type hints |
| **asyncio** | Built-in | Async runtime | Handles 3+ concurrent tasks efficiently |
| **Pydantic** | 2.x | Data validation | Type-based validation, automatic docs |

### External API Integration

| Technology | Version | Purpose | Why This Choice |
|-----------|---------|---------|-----------------|
| **httpx** | 0.25+ | Async HTTP client | Non-blocking API calls, timeouts |
| **python-notion-client** | Latest | Notion API | Official SDK, handles auth |
| **google-generativeai** | Latest | Gemini API | Official SDK, vision support |
| **python-telegram-bot** | 20.x | Telegram Bot API | Async support, webhooks |
| **requests** | 2.31+ | Sync HTTP (fallback) | Simple requests, well-tested |

### Android Automation

| Technology | Version | Purpose | Why This Choice |
|-----------|---------|---------|-----------------|
| **adb-shell** | 0.3+ | ADB protocol | Pure Python ADB client, no subprocess |
| **uiautomator2** | 3.x | UIAutomator2 | Python wrapper for Android automation |
| **pillow** | 10.x | Image processing | Screenshot analysis, image manipulation |
| **easyocr** | 1.7+ | OCR (optional) | Text extraction from screenshots |

### Database & Caching

| Technology | Version | Purpose | Why This Choice |
|-----------|---------|---------|-----------------|
| **SQLite** | 3.x | Local database | Built-in, no server needed, reliable |
| **SQLAlchemy** | 2.x | ORM | Type hints, migrations, query builder |
| **Alembic** | 1.13+ | Database migrations | Version control for schema changes |
| **Redis** | 7.x (optional) | Cache/queue | For scaling later, not needed for MVP |

### Logging & Monitoring

| Technology | Version | Purpose | Why This Choice |
|-----------|---------|---------|-----------------|
| **Loguru** | 0.7+ | Structured logging | Beautiful output, automatic rotation |
| **python-json-logger** | 2.x | JSON logs | Machine-readable, structured |

### Development Tools

| Technology | Version | Purpose | Why This Choice |
|-----------|---------|---------|-----------------|
| **pytest** | 7.x | Unit testing | Fixtures, parametrization, plugins |
| **pytest-asyncio** | 0.21+ | Async testing | Test async functions |
| **black** | 23.x | Code formatter | Python code style (auto-format) |
| **flake8** | 6.x | Linting | PEP8 compliance |
| **mypy** | 1.x | Type checking | Static type analysis |

---

## Android Device Stack

### ADB & Automation

| Tool | Version | Purpose | Why This Choice |
|------|---------|---------|-----------------|
| **Android ADB** | 35+ | Device protocol | Official SDK, reliable |
| **UIAutomator2** | 2.x | UI automation | Finds elements by resource_id, xpath |
| **Scrcpy** | 2.x | Screen mirroring | For manual override, debug |

### Android APIs

| API | Level | Purpose | Why This Choice |
|-----|-------|---------|-----------------|
| **SMS Manager** | 31+ | Send SMS | Native Android API |
| **Content Provider** | 31+ | Contact access | Query phone contacts |
| **Intent** | 31+ | App launching | Start MAX/WhatsApp/SMS |
| **Accessibility Service** | Optional | Typing input | Fallback for UIAutomator |

### Apps (Pre-installed on Devices)

| App | Version | Purpose | Support |
|-----|---------|---------|---------|
| **MAX** | 8.0+ | Messaging | Primary channel |
| **WhatsApp** | Latest | Messaging | Secondary channel |
| **SMS App** | System | SMS | Tertiary channel |
| **Chrome** | Latest | Scrcpy control | Manual debugging |

---

## External Services (APIs)

### Notion

```
Endpoint: https://api.notion.com/v1
Authentication: Bearer token (in .env)
Rate limits: 3 req/sec
Polling: 1/min (60 req/hour, well under limit)
Operations:
  • POST /databases/{id}/query (fetch leads)
  • PATCH /pages/{id} (update status)
  • PATCH /blocks/{id} (update checklist)
```

### Google Gemini

```
Endpoint: https://generativelanguage.googleapis.com/v1beta/...
Authentication: API key (in .env)
Rate limits: 2-15 req/min (depends on plan)
Operations:
  • POST /models/gemini-pro:generateContent (text generation)
  • POST /models/gemini-pro-vision:generateContent (vision)
Caching: Context file caching (save tokens)
Timeout: 30 sec max per request
```

### Telegram Bot

```
Endpoint: https://api.telegram.org/bot{token}/...
Authentication: Bot token (in .env)
Rate limits: 30 messages/sec
Operations:
  • POST /sendMessage (send log/alert)
  • POST /sendPhoto (send screenshot)
  • POST /editMessage (update status)
```

### RusProfile (Optional)

```
Endpoint: https://www.rusprofile.ru (no official API)
Method: Web scraping (BeautifulSoup)
Purpose: Fallback company data if Notion incomplete
Timeout: 10 sec
Headers: User-Agent (masquerade as browser)
```

---

## Infrastructure & Deployment

### Local Development

```
Machine: Mac (any recent model)
OS: macOS 12+
Disk: 100GB+ (for screenshots, logs)
RAM: 8GB minimum (16GB recommended for 20 devices)
Network: Local WiFi (for device connectivity)

USB Hub: ORICO USB 3.0 hub (10 ports)
Cables: USB-A to USB-C (20x, for devices)
Devices: 20x Google Pixel 5 or compatible
```

### Files & Directories

```
project/
├── frontend/                    # React app
│   ├── src/
│   │   ├── components/         # AlignUI components
│   │   ├── pages/              # Dashboard, Settings, etc
│   │   ├── services/           # Axios service layer
│   │   ├── store/              # Zustand state
│   │   └── theme/              # Design tokens
│   └── package.json
│
├── backend/                     # FastAPI app
│   ├── app/
│   │   ├── api/                # API routes
│   │   ├── services/           # Business logic
│   │   ├── agents/             # Android agents
│   │   ├── models/             # Pydantic models
│   │   ├── db/                 # Database layer
│   │   └── config.py           # Settings
│   ├── requirements.txt
│   ├── main.py                 # FastAPI app
│   └── .env.example
│
├── data/                        # Local data
│   ├── database.db             # SQLite
│   ├── logs/                   # Log files
│   ├── screenshots/            # Task screenshots
│   └── context/                # 20 .md files for Gemini
│
└── docker/                      # Optional Docker setup
    ├── Dockerfile              # Single container
    └── docker-compose.yml      # Frontend + Backend
```

### Environment Variables (.env)

```
# Notion
NOTION_API_KEY=ntn_...
NOTION_DATABASE_ID=...

# Gemini
GEMINI_API_KEY=...

# Telegram
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...

# Backend
BACKEND_HOST=localhost
BACKEND_PORT=8000
LOG_LEVEL=INFO

# Frontend
REACT_APP_API_URL=http://localhost:8000

# Features
ENABLE_SCREENSHOTS=true
ENABLE_WARMUP=true
MAX_CONCURRENT_DEVICES=3
DEVICE_HEALTH_CHECK_INTERVAL=30
```

---

## Dependencies Matrix

```
Frontend Dependencies:
  react ← vite, typescript
  zustand ← axios, react-query
  tailwind ← postcss, autoprefixer
  alignui ← react, typescript
  anime.js ← vanilla JS

Backend Dependencies:
  fastapi ← pydantic, starlette
  adb-shell ← socket, struct
  uiautomator2 ← adb-shell, json
  httpx ← asyncio, ssl
  sqlalchemy ← sqlite3
  loguru ← colorama

Device-side Dependencies (no install needed):
  Android Runtime (comes with Pixel)
  ADB Daemon (built-in)
  UIAutomator2 (built-in)
```

---

## Version Compatibility Matrix

| Component | Min Version | Max Version | Notes |
|-----------|------------|-----------|-------|
| Python | 3.9 | 3.12 | 3.11+ recommended |
| Node.js | 16 LTS | 22 LTS | Use LTS versions |
| React | 18.0 | 19.x | Type-safe |
| Android | 11 (API 30) | 14 (API 34) | Pixel 5 compatible |
| Notion API | v1 (latest) | v1 (latest) | No breaking changes expected |
| Gemini API | v1beta | v1 (when available) | Watch for updates |

---

## Performance Specifications

### Frontend

```
Bundle size: < 200 KB (gzipped)
Initial load: < 2 sec
Interaction response: < 100 ms
WebSocket latency: < 50 ms (local)
Memory usage: < 150 MB (chrome)
```

### Backend

```
Request handling: < 100 ms (avg)
Notion API call: 1-2 sec
Gemini API call: 2-5 sec
ADB command: < 1 sec (USB 3.0)
SQLite write: < 50 ms
Max concurrent: 3 executions
```

### Device

```
Message send: 60-70 sec (with HumanBehavior)
ADB ping: < 500 ms
Screenshot: < 2 sec
Screenshot size: 500-800 KB
Storage available: > 10 GB (for 20 devices logs)
```

---

## Security & Compliance

### Encryption

```
Data at Rest:
  • SQLite database: NOT encrypted (local file)
  • API keys: Stored in .env (not in git)
  • Screenshots: Plain files (local disk)
  
Data in Transit:
  • Frontend ← → Backend: HTTP (local, not exposed)
  • Backend → Notion API: HTTPS
  • Backend → Gemini API: HTTPS
  • Backend → Telegram API: HTTPS
  • Device ← → Backend: USB (local, no encryption)
```

### API Security

```
Notion:
  • API key in environment variable only
  • Never log full API key
  • Rate limit: 1 request/min (safe)
  
Gemini:
  • API key in environment variable only
  • Request timeout: 30 sec
  • Model: gemini-pro-vision (latest stable)
  
Telegram:
  • Bot token in environment variable only
  • Chat ID (logged): public info anyway
  • Message encryption: built-in by Telegram
```

---

## Monitoring & Debugging Tools

```
Frontend:
  • React DevTools (browser extension)
  • Redux DevTools (Zustand support)
  • Network tab (Chrome DevTools)
  • Console (debug logs)

Backend:
  • FastAPI Swagger UI (/docs)
  • Loguru output (console + file)
  • SQLite viewer (command-line: sqlite3)
  • Telegram logs (batch updates)

Device:
  • Scrcpy (screen mirror + control)
  • ADB logcat (device logs)
  • UIAutomator UI Dumper (inspect elements)
  • Android Studio (emulator, device manager)
```

---

## Upgrade & Maintenance Path

### Regular Updates

```
Monthly:
  • Check Notion API changelog
  • Update Gemini SDK (minor versions)
  • Review Telegram Bot API changes

Quarterly:
  • Update React/Node dependencies
  • Update Python dependencies
  • Update Android apps on devices
  
Yearly:
  • Major version upgrades (FastAPI 0.x → 1.x)
  • Security patches (critical)
  • Review and refactor tech choices
```

### Deprecation Plan

```
If Android version breaks:
  → Upgrade all devices to latest Android 14
  → Re-test all agents

If Notion API v1 deprecated:
  → Migrate to Notion API v2 (if available)
  → Update NotionSync service

If Gemini model changes:
  → Update context file paths
  → Retune prompts

If USB hub failure:
  → Replace with identical model (ORICO)
  → Re-seat all cables
```

---

## End of 11_TECH_STACK.md

Полный список всех технологий + версии + причины выбора.

Готов создать **файл 12 (Data Model)**?
