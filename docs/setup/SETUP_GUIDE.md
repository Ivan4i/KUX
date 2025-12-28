# 🚀 Setup Guide - Android Agent Platform

**Дата:** 2025-12-04
**Статус:** Ready for E2E Testing
**Цель:** Настроить окружение для отправки первых 2 WhatsApp сообщений

---

## 📋 Оглавление

1. [API Ключи](#1-api-ключи)
2. [Backend Configuration](#2-backend-configuration)
3. [Настройка Android Устройства](#3-настройка-android-устройства)
4. [Настройка Tailscale VPN](#4-настройка-tailscale-vpn)
5. [Настройка ADB](#5-настройка-adb)
6. [Создание Notion Database](#6-создание-notion-database)
7. [Запуск Приложения](#7-запуск-приложения)
8. [E2E Testing](#8-e2e-testing)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. API Ключи

### 1.1 Notion API Key

**Зачем нужно:** Синхронизация задач из Notion базы данных

**Как получить:**
1. Открыть https://www.notion.so/my-integrations
2. Нажать **"+ New integration"**
3. Заполнить форму:
   - Name: `Android Agent Platform`
   - Associated workspace: выбрать ваш workspace
   - Type: Internal
   - Capabilities:
     - ✅ Read content
     - ✅ Update content
     - ✅ Insert content
4. Нажать **"Submit"**
5. Скопировать **Internal Integration Token** (начинается с `secret_`)

**Формат:**
```
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 1.2 Notion Database ID

**Как получить:**
1. Открыть вашу Notion базу данных для WhatsApp задач
2. Нажать **"Share"** → **"Invite"** → выбрать вашу интеграцию
3. Скопировать URL базы данных:
   ```
   https://www.notion.so/{workspace}/{database_id}?v={view_id}
   ```
4. Database ID - это часть между workspace и `?v=`

**Формат:**
```
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Структура базы данных (обязательные колонки):**
- **Message ID** (Title) - уникальный ID задачи
- **Recipient Name** (Text) - имя получателя
- **Phone Number** (Phone) - номер телефона (формат: +66812345678)
- **Message Content** (Text) - текст сообщения
- **Status** (Select) - статус: Pending, Running, Sent, Failed
- **Device Assignment** (Select) - устройство: Auto, pixel-th-1, pixel-th-2, pixel-th-3
- **Priority** (Number) - приоритет (1-10, где 10 = highest)
- **Created Date** (Date) - дата создания
- **Sent Date** (Date) - дата отправки
- **Notes** (Text) - дополнительная информация

### 1.3 Telegram Bot Token

**Зачем нужно:** Уведомления о статусе задач

**Как получить:**
1. Открыть Telegram → найти **@BotFather**
2. Отправить команду `/newbot`
3. Указать имя бота: `Android Agent Notifier`
4. Указать username: `android_agent_notifier_bot` (должен быть уникальным)
5. Получите токен в формате `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

**Формат:**
```
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 1.4 Telegram Chat ID

**Как получить:**
1. Добавить вашего бота в чат или написать ему `/start`
2. Открыть в браузере:
   ```
   https://api.telegram.org/bot{YOUR_BOT_TOKEN}/getUpdates
   ```
3. Найти `"chat":{"id":123456789}` в ответе
4. Скопировать числовой ID

**Формат:**
```
TELEGRAM_CHAT_ID=123456789
```

### 1.5 Puter.js API Key

**Зачем нужно:** LLM для персонализации сообщений и DroidRun AI automation

**Как получить:**
1. Открыть https://puter.com
2. Зарегистрироваться / войти
3. Перейти в Settings → API Keys
4. Создать новый API key
5. Скопировать ключ

**Формат:**
```
PUTER_API_KEY=your_puter_api_key_here
```

**Note:** Если Puter.js недоступен, можно использовать другой LLM API (OpenAI, Anthropic, etc.) - потребуется изменить код в `puter_client.py`

---

## 2. Backend Configuration

### 2.1 Создать .env файл

```bash
cd backend
cp .env.example .env
```

### 2.2 Заполнить .env

Открыть `backend/.env` и заполнить API ключи:

```env
# Notion API
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Telegram Bot
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789

# Puter.js LLM API
PUTER_API_KEY=your_puter_api_key_here
PUTER_API_URL=https://api.puter.ai/v1
PUTER_DEFAULT_MODEL=claude-sonnet-4.5

# Database
DATABASE_URL=sqlite:///./data/android_agent.db

# General
APP_ENV=development
APP_DEBUG=true
LOG_LEVEL=INFO

# Device Configuration
DEVICE_CONFIG_PATH=../config/devices.yaml

# ADB / Tailscale
ADB_HOST=localhost
ADB_PORT=5037
```

---

## 3. Настройка Android Устройства

### 3.1 Требования к устройству

**Временное устройство (любой Android):**
- Android 8.0+ (API 26+)
- Минимум 2GB RAM
- Wi-Fi соединение
- Зарядка (рекомендуется подключить к источнику питания)

**Target устройства (Google Pixel 5):**
- Android 11+
- 8GB RAM
- Snapdragon 765G
- Оптимизировано для длительной работы

### 3.2 Включить Developer Options

1. **Открыть Settings** → **About phone**
2. **Найти "Build number"**
3. **Тапнуть 7 раз** на Build number
4. Появится сообщение "You are now a developer!"

### 3.3 Включить USB Debugging

1. **Settings** → **Developer options**
2. Включить **"Developer options"** (переключатель вверху)
3. Включить **"USB debugging"**
4. Включить **"Stay awake"** (экран не гаснет при зарядке)

### 3.4 Включить Wireless ADB (для удаленного доступа)

**Метод 1: ADB over Wi-Fi (Android 11+)**
1. **Settings** → **Developer options**
2. Включить **"Wireless debugging"**
3. Нажать на "Wireless debugging"
4. Запомнить **IP address and port** (например: `192.168.1.100:5555`)

**Метод 2: ADB через USB → Wireless (любой Android)**
1. Подключить устройство через USB к компьютеру
2. Выполнить на компьютере:
   ```bash
   adb devices  # Проверить что устройство видно
   adb tcpip 5555  # Включить ADB по TCP/IP
   adb connect 192.168.1.100:5555  # Подключиться по Wi-Fi
   ```
3. Теперь можно отключить USB кабель

### 3.5 Установить WhatsApp

1. Открыть **Google Play Store**
2. Найти **"WhatsApp"**
3. Установить
4. Авторизоваться с вашим номером телефона
5. **Важно:** Использовать отдельный номер для тестирования, не основной!

### 3.6 Отключить Battery Optimization

1. **Settings** → **Apps** → **WhatsApp**
2. **Battery** → **Battery optimization**
3. Выбрать **"Don't optimize"** для WhatsApp
4. То же самое для **Tailscale** (когда установите)

---

## 4. Настройка Tailscale VPN

**Зачем нужно:** Удаленный доступ к Android устройству через ADB over Tailscale

### 4.1 Установить Tailscale на Android

1. Открыть **Google Play Store**
2. Найти **"Tailscale"**
3. Установить
4. Запустить → Войти с вашим Tailscale аккаунтом
5. Разрешить VPN соединение

### 4.2 Включить SSH/ADB в Tailscale

1. В Tailscale app → **Settings**
2. Включить **"Accept routes"**
3. Включить **"Exit node"** (optional)

### 4.3 Получить Tailscale IP адрес устройства

1. В Tailscale app → главный экран
2. Скопировать **IP address** (формат: `100.x.x.x`)
3. Этот IP будет использоваться для ADB подключения

**Пример:**
```
Tailscale IP: 100.101.102.103
```

### 4.4 Установить Tailscale на компьютере (backend server)

**MacOS:**
```bash
brew install tailscale
sudo tailscale up
```

**Ubuntu/Debian:**
```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

**Проверка:**
```bash
tailscale status
# Должны увидеть ваш Android устройство в списке
```

---

## 5. Настройка ADB

### 5.1 Установить ADB на компьютере

**MacOS:**
```bash
brew install android-platform-tools
```

**Ubuntu/Debian:**
```bash
sudo apt-get install android-tools-adb
```

### 5.2 Подключиться к Android через Tailscale

```bash
# Проверить что ADB сервер запущен
adb start-server

# Подключиться к устройству через Tailscale IP
adb connect 100.101.102.103:5555

# Проверить подключение
adb devices
# Должно показать:
# 100.101.102.103:5555    device
```

**Если запрашивает подтверждение на Android:**
- На экране устройства появится popup "Allow USB debugging?"
- Отметить **"Always allow from this computer"**
- Нажать **"OK"**

### 5.3 Проверить доступ к WhatsApp

```bash
# Запустить WhatsApp
adb shell am start -n com.whatsapp/com.whatsapp.HomeActivity

# Проверить что WhatsApp запущен
adb shell dumpsys window windows | grep -i whatsapp

# Сделать скриншот (проверка)
adb shell screencap -p /sdcard/test.png
adb pull /sdcard/test.png ~/Desktop/test.png
```

---

## 6. Создание Notion Database

### 6.1 Создать новую базу данных

1. Открыть Notion → создать новую страницу
2. Добавить **"Table - Full page"**
3. Назвать: **"WhatsApp Outreach Tasks"**

### 6.2 Создать колонки (Properties)

| Property Name | Type | Options |
|--------------|------|---------|
| Message ID | Title | - |
| Recipient Name | Text | - |
| Phone Number | Phone | - |
| Message Content | Text | - |
| Status | Select | Pending, Running, Sent, Failed |
| Device Assignment | Select | Auto, pixel-th-1, pixel-th-2, pixel-th-3 |
| Priority | Number | Min: 1, Max: 10 |
| Created Date | Date | - |
| Sent Date | Date | - |
| Notes | Text | - |

### 6.3 Добавить тестовые задачи

**Task 1:**
- Message ID: `TEST-001`
- Recipient Name: `Test Contact 1`
- Phone Number: `+66812345678` (замените на реальный тестовый номер)
- Message Content: `Hello! This is a test message from Android Agent Platform. Please confirm receipt.`
- Status: `Pending`
- Device Assignment: `Auto`
- Priority: `10`

**Task 2:**
- Message ID: `TEST-002`
- Recipient Name: `Test Contact 2`
- Phone Number: `+66898765432` (замените на другой тестовый номер)
- Message Content: `Hi! Testing WhatsApp automation. This message was sent automatically via ADB.`
- Status: `Pending`
- Device Assignment: `Auto`
- Priority: `9`

### 6.4 Подключить интеграцию

1. В базе данных → **"⋯"** (верхний правый угол) → **"Connections"**
2. Нажать **"Connect to"** → выбрать вашу интеграцию
3. Нажать **"Confirm"**

---

## 7. Запуск Приложения

### 7.1 Обновить devices.yaml

Открыть `config/devices.yaml` и настроить ваше устройство:

**Для временного Android устройства:**
```yaml
devices:
  - id: android-test-1
    name: "Test Android Device"
    tailscale_ip: "100.101.102.103"  # ВАШ Tailscale IP
    adb_port: 5555
    location: "Local"
    timezone: "Asia/Bangkok"
    enabled: true
```

**Когда придут Google Pixel 5:**
```yaml
devices:
  - id: pixel-th-1
    name: "Pixel 5 - Thailand Device 1"
    tailscale_ip: "100.x.x.x"  # Обновить когда настроите
    adb_port: 5555
    location: "Thailand"
    timezone: "Asia/Bangkok"
    enabled: true

  - id: pixel-th-2
    name: "Pixel 5 - Thailand Device 2"
    tailscale_ip: "100.x.x.x"
    adb_port: 5555
    location: "Thailand"
    timezone: "Asia/Bangkok"
    enabled: true

  - id: pixel-th-3
    name: "Pixel 5 - Thailand Device 3"
    tailscale_ip: "100.x.x.x"
    adb_port: 5555
    location: "Thailand"
    timezone: "Asia/Bangkok"
    enabled: true
```

### 7.2 Запустить Backend

```bash
# Открыть Terminal 1
cd backend

# Активировать venv
source venv/bin/activate

# Запустить backend
python -m uvicorn src.main:app --reload --port 8000
```

**Ожидаемый вывод:**
```
🚀 Starting Android Agent Platform Backend...
📊 Initializing database...
✅ Database initialized
📱 Initializing Device Manager...
🔗 Connecting to device: android-test-1 (100.101.102.103:5555)
✅ Device Manager initialized
🎉 Backend startup complete!
============================================================
🤖 Android Agent Platform Backend
============================================================
📝 Docs: http://localhost:8000/docs
🏥 Health: http://localhost:8000/api/health
============================================================
```

**Проверить health:**
```bash
curl http://localhost:8000/api/health
```

### 7.3 Запустить Frontend

```bash
# Открыть Terminal 2
cd frontend

# Установить dependencies (если еще не установлены)
npm install

# Запустить dev server
npm run dev
```

**Ожидаемый вывод:**
```
  VITE v5.x.x  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### 7.4 Открыть Dashboard

Открыть в браузере: **http://localhost:5173**

**Должны увидеть:**
- ✅ Dashboard загружается
- ✅ Device Card показывает ваше устройство (android-test-1)
- ✅ Status: online (зеленый)
- ✅ Battery, temperature, memory metrics

---

## 8. E2E Testing

### 8.1 Проверка подключения устройства

**В Dashboard:**
1. Проверить что устройство **online**
2. Нажать на device card → проверить metrics
3. Нажать **"Refresh"** → status должен обновиться

**Альтернативно через API:**
```bash
# Получить список устройств
curl http://localhost:8000/api/devices

# Получить статус конкретного устройства
curl http://localhost:8000/api/devices/android-test-1/status

# Сделать screenshot (проверка ADB доступа)
curl http://localhost:8000/api/devices/android-test-1/screenshot
```

### 8.2 Синхронизация задач из Notion

**В Dashboard:**
1. Нажать кнопку **"Sync Notion"**
2. Дождаться завершения (spinner исчезнет)
3. Проверить что появились 2 задачи в списке

**Ожидаемый результат:**
- Success notification
- Tasks synced: 2

**Через API:**
```bash
# Синхронизировать задачи
curl -X POST http://localhost:8000/api/tasks/sync-notion?limit=10

# Проверить задачи в базе
curl http://localhost:8000/api/tasks?status=Pending
```

### 8.3 Отправка WhatsApp сообщения

**ВАЖНО: Убедитесь что:**
- ✅ WhatsApp авторизован на устройстве
- ✅ Тестовые контакты сохранены в WhatsApp
- ✅ Устройство разблокировано
- ✅ Экран включен

**В Dashboard:**
1. Нажать кнопку **"Run Task"**
2. Наблюдать real-time progress в секции **"Current Activity"**:
   - Opening WhatsApp...
   - Finding contact...
   - Typing message...
   - Sending message...
   - Verifying delivery...
3. Проверить результат:
   - ✅ Current Activity показывает "Task completed"
   - ✅ Recent Logs показывает success entry
   - ✅ Notion status обновился на "Sent"
   - ✅ Telegram уведомление получено

**Проверка на устройстве:**
1. Открыть WhatsApp на Android устройстве
2. Найти чат с тестовым контактом
3. Убедиться что сообщение отправлено ✅
4. Проверить двойную галочку (delivered)

### 8.4 Отправка второго сообщения

Повторить пункт 8.3 для второй задачи.

### 8.5 Success Criteria

**MVP считается успешным если:**
- ✅ Backend запущен без ошибок
- ✅ Frontend загружается и показывает данные
- ✅ Device Manager видит Android устройство
- ✅ ADB connection работает (можем делать screenshots)
- ✅ Notion sync загружает задачи
- ✅ WebSocket real-time updates работают
- ✅ **2 WhatsApp сообщения отправлены успешно**
- ✅ Notion statuses обновились на "Sent"
- ✅ Telegram notifications получены
- ✅ Logs сохранены в database

---

## 9. Troubleshooting

### 9.1 Backend не запускается

**Ошибка: "ModuleNotFoundError"**
```bash
# Убедиться что venv активирован
source venv/bin/activate

# Переустановить dependencies
pip install -r requirements.txt
```

**Ошибка: "AttributeError: DeviceManager has no method..."**
- Эта ошибка была исправлена в Phase 0
- Убедитесь что используете последнюю версию кода

### 9.2 ADB не подключается к устройству

**Ошибка: "failed to connect to 100.x.x.x:5555"**

1. Проверить Tailscale:
   ```bash
   tailscale status
   # Должно показать устройство online
   ```

2. Проверить что Wireless ADB включен на Android:
   ```bash
   # Попробовать другой порт
   adb connect 100.x.x.x:37267  # Wireless debugging default port
   ```

3. Перезапустить ADB server:
   ```bash
   adb kill-server
   adb start-server
   adb connect 100.x.x.x:5555
   ```

4. Проверить firewall на Android устройстве

### 9.3 WhatsApp automation не работает

**Сообщение не отправляется:**

1. Проверить что WhatsApp открыт:
   ```bash
   adb shell am start -n com.whatsapp/com.whatsapp.HomeActivity
   ```

2. Проверить что контакт существует в WhatsApp:
   - Откройте WhatsApp вручную
   - Найдите контакт по номеру телефона
   - Убедитесь что контакт сохранен

3. Проверить формат номера телефона:
   - Должен начинаться с "+" и country code
   - Пример: `+66812345678` (Thailand)
   - БЕЗ пробелов, скобок, дефисов

4. Посмотреть logs:
   ```bash
   # Backend logs
   tail -f backend/logs/app.log
   ```

5. Сделать screenshot для debugging:
   ```bash
   curl http://localhost:8000/api/devices/android-test-1/screenshot
   ```

### 9.4 Notion sync не работает

**Ошибка: "401 Unauthorized"**
- Проверить NOTION_API_KEY в .env
- Убедиться что интеграция подключена к database

**Ошибка: "404 Not Found"**
- Проверить NOTION_DATABASE_ID в .env
- Убедиться что ID правильный (из URL базы данных)

**No tasks found:**
- Проверить что Status = "Pending" в Notion
- Проверить что задачи существуют в базе

### 9.5 Frontend ошибки

**Dashboard не загружается:**
- Проверить что backend запущен (http://localhost:8000/api/health)
- Проверить browser console (F12) для ошибок
- Проверить что CORS настроен правильно в main.py

**WebSocket connection failed:**
- Проверить что backend WebSocket endpoint работает
- Проверить firewall settings

### 9.6 Device показывает "offline"

1. Проверить ADB connection:
   ```bash
   adb devices
   ```

2. Переподключиться:
   ```bash
   adb disconnect 100.x.x.x:5555
   adb connect 100.x.x.x:5555
   ```

3. Проверить Tailscale connection
4. Перезапустить backend

---

## 🎯 Следующие шаги после E2E testing

После успешной отправки 2 WhatsApp сообщений:

1. **Настроить Google Pixel 5 устройства** (когда придут):
   - Повторить шаги 3-5 для каждого Pixel
   - Обновить devices.yaml с реальными Tailscale IPs
   - Настроить Tailscale auto-start on boot

2. **Phase 3: Testing Infrastructure**:
   - Создать pytest unit tests
   - Integration tests для API endpoints
   - Mock tests для ADB/Notion/Telegram

3. **Phase 4: Production Readiness**:
   - PostgreSQL migration
   - Docker containerization
   - CI/CD pipeline
   - Monitoring & logging

4. **Phase 5: Advanced Features (Slice 2)**:
   - Queue Manager (3 устройства параллельно)
   - Retry Manager с exponential backoff
   - Recovery Agent (5-level recovery)
   - Background Notion sync

---

## 📞 Support

Если возникли проблемы:
1. Проверить [Troubleshooting](#9-troubleshooting)
2. Посмотреть logs: `backend/logs/app.log`
3. Проверить [PROGRESS.md](PROGRESS.md) для текущего статуса
4. Посмотреть API docs: http://localhost:8000/docs

---

**Good luck with E2E testing! 🚀**
