# 🚀 Quick Start Guide - Android Agent Platform

**Версия:** 1.0.0 (Slice 1 MVP)
**Статус:** 93% Complete - Ready for Testing
**Дата:** 2025-12-04

---

## ⚡ Быстрый старт

### Предварительные требования

- **Python 3.11+** установлен
- **Node.js 18+** установлен
- **ADB** установлен (Android Debug Bridge)
- **Tailscale** установлен и настроен
- **3 Google Pixel 5 устройства** во Вьетнаме/Таиланде с Tailscale
- **API ключи:**
  - Notion API key + Database ID
  - Telegram Bot Token (уже есть: `7695092594:AAFc0_3gPhzRJLNN49jtDcDbdzWWRLdfPjs`)
  - Puter.js API key

---

## 📦 Шаг 1: Установка Backend

```bash
cd backend

# Создать виртуальное окружение
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Создать .env файл
cp .env.example .env

# Отредактировать .env (добавить API ключи)
nano .env
```

### Пример .env файла:

```env
# Application
APP_ENV=development
APP_DEBUG=True
LOG_LEVEL=INFO

# Notion API
NOTION_API_KEY=secret_xxxxxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxxxxxxx

# Telegram Bot
TELEGRAM_BOT_TOKEN=7695092594:AAFc0_3gPhzRJLNN49jtDcDbdzWWRLdfPjs
TELEGRAM_CHAT_ID=your_chat_id

# Puter.js LLM API
PUTER_API_KEY=your_puter_key
PUTER_API_URL=https://api.puter.ai/v1
PUTER_DEFAULT_MODEL=claude-sonnet-4.5

# Database
DATABASE_URL=sqlite:///./data/sqlite.db

# Device Configuration
DEVICE_CONFIG_PATH=../config/devices.yaml
```

### Инициализировать базу данных:

```bash
# Создать папку для БД
mkdir -p data

# Запустить скрипт инициализации
python scripts/init_db.py
```

---

## 📦 Шаг 2: Установка Frontend

```bash
cd ../frontend

# Установить зависимости
npm install

# Создать .env файл
cp .env.example .env

# Отредактировать .env (опционально, по умолчанию использует localhost)
nano .env
```

### Пример .env файла:

```env
# Backend API URL
VITE_API_URL=http://localhost:8000

# WebSocket URL (without protocol)
VITE_WS_URL=localhost:8000
```

---

## 🔧 Шаг 3: Настройка устройств

Отредактировать `/config/devices.yaml`:

```yaml
devices:
  - id: pixel-th-1
    name: Pixel-TH-1
    location: Bangkok, Thailand
    timezone: Asia/Bangkok
    tailscale_ip: 100.64.1.101  # Замените на реальный Tailscale IP
    adb_port: 5555
    active_hours: "08:00-22:00"
    max_tasks_per_day: 50

  - id: pixel-vn-1
    name: Pixel-VN-1
    location: Ho Chi Minh, Vietnam
    timezone: Asia/Ho_Chi_Minh
    tailscale_ip: 100.64.1.102  # Замените на реальный Tailscale IP
    adb_port: 5555
    active_hours: "08:00-22:00"
    max_tasks_per_day: 50

  - id: pixel-th-2
    name: Pixel-TH-2
    location: Bangkok, Thailand
    timezone: Asia/Bangkok
    tailscale_ip: 100.64.1.103  # Замените на реальный Tailscale IP
    adb_port: 5555
    active_hours: "08:00-22:00"
    max_tasks_per_day: 30
```

---

## 🚀 Шаг 4: Запуск приложения

### Terminal 1 - Backend:

```bash
cd backend
source venv/bin/activate
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Проверить здоровье backend:**
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "ok",
  "service": "Android Agent Platform",
  "version": "1.0.0"
}
```

### Terminal 2 - Frontend:

```bash
cd frontend
npm run dev
```

Frontend will be available at: **http://localhost:3000**

---

## ✅ Шаг 5: Проверка подключения устройств

### Тест ADB подключения:

```bash
cd backend
source venv/bin/activate
python scripts/test_connection.py
```

Expected output:
```
✅ Connected to Pixel-TH-1
✅ Connected to Pixel-VN-1
✅ Connected to Pixel-TH-2
```

### Проверка через API:

```bash
curl http://localhost:8000/api/devices
```

Должно вернуть список устройств с их статусами.

---

## 📝 Шаг 6: Настройка Notion

### Создать таблицу в Notion:

Создайте базу данных в Notion со следующими колонками:

| Колонка | Тип | Обязательна |
|---------|-----|-------------|
| Message ID | Title | ✅ |
| Recipient Name | Text | ✅ |
| Phone Number | Text | ✅ |
| Message Content | Text | ✅ |
| Status | Status | ✅ |
| Device Assignment | Select | ✅ |
| Priority | Number | - |
| Created Date | Date | - |
| Scheduled Send Time | Date | - |
| Sent Date | Date | - |
| Attempt Count | Number | - |
| Notes | Text | - |

### Статусы (Status property):

- `Pending` - не отправлено
- `Running` - в процессе
- `Sent` - отправлено
- `Failed` - ошибка

### Device Assignment options:

- `Auto` - автоматический выбор устройства
- `Pixel-TH-1`
- `Pixel-VN-1`
- `Pixel-TH-2`

### Получить Database ID:

1. Откройте таблицу в Notion
2. URL будет выглядеть так: `https://www.notion.so/xxxxxxxxxxxxx?v=yyyyy`
3. `xxxxxxxxxxxxx` - это ваш Database ID

---

## 🎯 Шаг 7: Первый тест (E2E)

### 1. Добавить тестовые задачи в Notion:

Создайте 2 записи в Notion таблице:

**Задача 1:**
- Recipient Name: Test User 1
- Phone Number: +66812345678 (ваш тестовый номер)
- Message Content: Hello! This is a test message from Android Agent Platform.
- Status: Pending
- Device Assignment: Auto
- Priority: 10

**Задача 2:**
- Recipient Name: Test User 2
- Phone Number: +66812345679 (ваш тестовый номер)
- Message Content: Hi! This is the second test message.
- Status: Pending
- Device Assignment: Auto
- Priority: 9

### 2. Открыть Dashboard:

Перейдите на **http://localhost:3000**

Вы должны увидеть:
- 3 Device Cards (online/offline status)
- Current Activity (пустая)
- Recent Logs (пустые)

### 3. Синхронизировать Notion:

Нажмите кнопку **"Sync Notion"**

Должно появиться сообщение о синхронизации 2 задач.

### 4. Запустить первую задачу:

Нажмите кнопку **"Run Task"**

Вы должны увидеть:
- Current Activity заполняется данными о задаче
- Real-time progress updates (Opening WhatsApp, Finding contact, Typing message, Sending...)
- Recent Logs добавляются новые записи

### 5. Проверить результат:

- Проверьте телефон в Таиланде - сообщение должно быть отправлено
- Проверьте Notion - статус должен измениться на "Sent"
- Проверьте Telegram - должно прийти уведомление

### 6. Запустить вторую задачу:

Повторите шаг 4 для второй задачи.

---

## 🐛 Troubleshooting

### Backend не запускается:

```bash
# Проверить Python версию
python --version  # должно быть 3.11+

# Переустановить зависимости
pip install -r requirements.txt --force-reinstall

# Проверить логи
tail -f backend/logs/app.log
```

### Frontend не запускается:

```bash
# Очистить кеш
rm -rf node_modules package-lock.json
npm install

# Проверить Node версию
node --version  # должно быть 18+
```

### ADB не подключается к устройствам:

```bash
# Проверить Tailscale
tailscale status

# Проверить ADB
adb devices

# Подключиться вручную
adb connect 100.64.1.101:5555
```

### WebSocket не работает:

1. Проверить что backend запущен
2. Открыть Developer Console в браузере
3. Проверить ошибки WebSocket
4. Проверить что порт 8000 не заблокирован

### Notion API ошибки:

- Проверить API key
- Проверить Database ID
- Убедиться что API интеграция добавлена к database
- Проверить permissions

---

## 📚 Полезные ссылки

- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/health
- **Frontend:** http://localhost:3000
- **WebSocket:** ws://localhost:8000/ws

---

## 🎉 Success!

Если все шаги выполнены успешно, у вас работает:

✅ Backend API (FastAPI)
✅ Frontend Dashboard (React)
✅ WebSocket real-time updates
✅ Device Manager (ADB подключения)
✅ WhatsApp Agent (DroidRun automation)
✅ Notion integration
✅ Telegram notifications
✅ Human Behavior emulation

**Готово к Production testing!**

Следующий шаг: **Slice 2** - Full WhatsApp Flow с очередями, retry logic, и recovery agent.

---

*Создано: 2025-12-04 | Version: 1.0.0 (Slice 1 MVP)*
