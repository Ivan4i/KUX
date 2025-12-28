# 📋 Next Steps - Финализация MVP

**Статус:** 93% Complete (13/14 tasks)
**Последняя задача:** E2E Testing

---

## 🎯 Что нужно сделать для запуска

### 1. Получить API ключи ✅

#### Notion API:
1. Перейти на https://www.notion.so/my-integrations
2. Создать новую интеграцию
3. Скопировать "Internal Integration Token"
4. Создать базу данных в Notion (см. QUICKSTART.md)
5. Поделиться базой данных с интеграцией
6. Скопировать Database ID из URL

#### Telegram Bot:
- ✅ **Уже есть:** `7695092594:AAFc0_3gPhzRJLNN49jtDcDbdzWWRLdfPjs`
- Нужно получить Chat ID:
  1. Запустить бота в Telegram
  2. Отправить любое сообщение
  3. Открыть: `https://api.telegram.org/bot<TOKEN>/getUpdates`
  4. Найти `"chat":{"id":123456789}` - это ваш Chat ID

#### Puter.js API:
1. Зарегистрироваться на Puter.js (или аналогичном LLM API провайдере)
2. Получить API key
3. **ВАЖНО:** Убедиться что API поддерживает явное указание модели

---

### 2. Настроить устройства 📱

#### Подготовить Google Pixel 5:

**На каждом устройстве:**
1. Включить Developer Options
2. Включить USB Debugging
3. Включить Wireless ADB (Settings → Developer Options → Wireless debugging)
4. Установить WhatsApp
5. Авторизоваться в WhatsApp с отдельным номером телефона
6. Установить Tailscale
7. Подключиться к Tailscale VPN

#### Получить Tailscale IP:

На каждом устройстве открыть Tailscale и найти IP адрес (например: `100.64.1.101`)

#### Обновить `config/devices.yaml`:

```yaml
devices:
  - id: pixel-th-1
    name: Pixel-TH-1
    location: Bangkok, Thailand
    timezone: Asia/Bangkok
    tailscale_ip: 100.64.1.101  # ← ЗАМЕНИТЬ НА РЕАЛЬНЫЙ IP
    adb_port: 5555
    active_hours: "08:00-22:00"
    max_tasks_per_day: 50
```

#### Тест подключения:

```bash
# С вашего компьютера (тоже должен быть в Tailscale)
adb connect 100.64.1.101:5555
adb devices
```

Должно показать: `100.64.1.101:5555    device`

---

### 3. Создать .env файлы 🔐

#### Backend `.env`:

```bash
cd backend
cp .env.example .env
nano .env
```

Заполнить:
```env
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxx
TELEGRAM_BOT_TOKEN=7695092594:AAFc0_3gPhzRJLNN49jtDcDbdzWWRLdfPjs
TELEGRAM_CHAT_ID=123456789
PUTER_API_KEY=your_puter_key
PUTER_API_URL=https://api.puter.ai/v1
PUTER_DEFAULT_MODEL=claude-sonnet-4.5
```

#### Frontend `.env`:

```bash
cd frontend
cp .env.example .env
# Обычно не требует изменений для локального запуска
```

---

### 4. Установить зависимости 📦

#### Backend:

```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend:

```bash
cd frontend
npm install
```

---

### 5. Инициализировать базу данных 💾

```bash
cd backend
source venv/bin/activate
mkdir -p data
python scripts/init_db.py
```

Должно создать файл `backend/data/sqlite.db`

---

### 6. Запустить приложение 🚀

#### Terminal 1 - Backend:

```bash
cd backend
source venv/bin/activate
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Проверка:**
```bash
curl http://localhost:8000/api/health
# Ожидается: {"status":"ok","service":"Android Agent Platform","version":"1.0.0"}
```

#### Terminal 2 - Frontend:

```bash
cd frontend
npm run dev
```

**Открыть:** http://localhost:3000

---

### 7. Создать Notion таблицу 📝

#### Структура таблицы:

| Property Name | Type | Options |
|--------------|------|---------|
| Message ID | Title | - |
| Recipient Name | Text | - |
| Phone Number | Text | - |
| Message Content | Text | - |
| Status | Status | Pending, Running, Sent, Failed |
| Device Assignment | Select | Auto, Pixel-TH-1, Pixel-VN-1, Pixel-TH-2 |
| Priority | Number | - |
| Created Date | Date | - |
| Scheduled Send Time | Date | - |
| Sent Date | Date | - |
| Attempt Count | Number | - |
| Notes | Text | - |

#### Добавить тестовые данные:

**Запись 1:**
- Message ID: Test 1
- Recipient Name: Your Name
- Phone Number: +66812345678 (ваш тестовый номер)
- Message Content: Hello! This is a test message from Android Agent Platform. Testing MVP.
- Status: Pending
- Device Assignment: Auto
- Priority: 10

**Запись 2:**
- Message ID: Test 2
- Recipient Name: Your Name
- Phone Number: +66812345678
- Message Content: Hi! This is the second test message. Everything is working!
- Status: Pending
- Device Assignment: Auto
- Priority: 9

---

### 8. Запустить E2E тест ✅

#### Шаг 1: Проверить Dashboard

Открыть http://localhost:3000

Должно быть видно:
- 3 Device Cards (могут быть offline если устройства не подключены)
- Current Activity (пусто)
- Recent Logs (пусто)
- Кнопки: Sync Notion, Run Task, Refresh

#### Шаг 2: Sync Notion

1. Нажать **"Sync Notion"**
2. В консоли браузера (F12) должны появиться логи
3. Должно загрузиться 2 задачи из Notion

Проверить через API:
```bash
curl http://localhost:8000/api/tasks
```

#### Шаг 3: Проверить устройства

```bash
curl http://localhost:8000/api/devices
```

Должно показать 3 устройства. Если все offline - проверить:
- Tailscale подключение
- ADB подключение
- devices.yaml конфигурацию

#### Шаг 4: Запустить первую задачу

1. Нажать **"Run Task"**
2. Наблюдать real-time обновления:
   - Current Activity заполняется
   - Progress updates появляются
   - Logs добавляются
3. WebSocket должен показывать:
   - `task_started`
   - `task_progress` ("Opening WhatsApp...", "Finding contact...", "Typing message...", "Sending...")
   - `task_completed` или `task_failed`

#### Шаг 5: Проверить результаты

**На телефоне в Таиланде:**
- Открыть WhatsApp
- Проверить что сообщение получено

**В Notion:**
- Обновить страницу
- Статус должен измениться на "Sent"
- Sent Date должен быть заполнен

**В Telegram:**
- Должно прийти уведомление:
  - "✅ WhatsApp Message Sent"
  - С деталями: Recipient, Phone, Device, Duration

**В Dashboard:**
- Recent Logs должны показать успешную отправку
- Device Card должен увеличить "Tasks today" на 1

#### Шаг 6: Запустить вторую задачу

Повторить шаг 4 для второй задачи.

---

## ✅ Success Criteria

Slice 1 считается **полностью завершенным** когда:

- [x] Backend запущен и отвечает на `/api/health`
- [x] Frontend запущен на `http://localhost:3000`
- [x] Все 3 устройства показывают статус (хотя бы 1 online)
- [x] Notion sync загружает задачи
- [x] WebSocket подключен (в консоли браузера видно "WebSocket connected")
- [ ] **Задача 1 отправлена успешно:**
  - [ ] Сообщение получено на телефоне
  - [ ] Notion статус = "Sent"
  - [ ] Telegram уведомление получено
  - [ ] Logs сохранены в БД
- [ ] **Задача 2 отправлена успешно:**
  - [ ] Сообщение получено на телефоне
  - [ ] Notion статус = "Sent"
  - [ ] Telegram уведомление получено
  - [ ] Logs сохранены в БД

---

## 🐛 Troubleshooting

### Проблема: Backend не запускается

**Ошибка:** `ModuleNotFoundError`
```bash
pip install -r requirements.txt --force-reinstall
```

**Ошибка:** `Permission denied` для sqlite.db
```bash
chmod 755 backend/data
chmod 644 backend/data/sqlite.db
```

### Проблема: Устройства offline

**Проверить Tailscale:**
```bash
tailscale status
ping 100.64.1.101
```

**Проверить ADB:**
```bash
adb devices
adb connect 100.64.1.101:5555
```

**Перезапустить ADB на телефоне:**
Settings → Developer Options → Wireless Debugging → выключить и включить

### Проблема: Notion API ошибки

**Ошибка 401 (Unauthorized):**
- Проверить API key
- Убедиться что интеграция добавлена к базе данных

**Ошибка 404 (Not Found):**
- Проверить Database ID
- Убедиться что база данных существует

### Проблема: WhatsApp Agent не работает

**Проверить что на устройстве:**
- WhatsApp установлен и авторизован
- Устройство разблокировано
- Экран включен

**Проверить логи:**
```bash
tail -f backend/logs/app.log
```

### Проблема: WebSocket не подключается

**В консоли браузера (F12):**
- Проверить ошибки WebSocket
- URL должен быть `ws://localhost:8000/ws`

**Проверить что backend запущен:**
```bash
curl http://localhost:8000/api/health
```

---

## 📊 После успешного E2E теста

Когда обе задачи отправлены успешно:

1. **Обновить PROGRESS.md:**
   - Задача 14: ✅ Завершено
   - Прогресс: 100% (14/14)

2. **Создать git commit:**
   ```bash
   git add .
   git commit -m "🎉 Slice 1 MVP Complete - E2E test passed"
   ```

3. **Задокументировать результаты:**
   - Screenshots Dashboard
   - Logs из backend
   - Примеры отправленных сообщений

4. **Готовиться к Slice 2:**
   - Queue Manager
   - Retry Logic
   - Recovery Agent
   - Enhanced Human Behavior

---

## 🚀 Next Phase: Slice 2

После завершения Slice 1, следующие задачи (см. ROADMAP.md):

1. Queue Manager (priority queue, load balancing)
2. Retry Manager (exponential backoff, 3 attempts)
3. Recovery Agent (5-level error recovery)
4. Enhanced Human Behavior (typos, warmup mode, active hours)
5. Background Notion Sync (every 60 sec)
6. Enhanced Telegram Bot (interactive buttons)
7. Task Scheduler (cron-like)
8. Health Monitor (background monitoring)

**Ожидаемая длительность Slice 2:** 7 дней

---

*Удачи с тестированием! 🚀*
