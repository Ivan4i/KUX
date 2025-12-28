# API Reference - Полная документация API

## Обзор

**Base URL:** `http://localhost:8000`

**WebSocket:** `ws://localhost:8000/ws`

**Swagger Docs:** `http://localhost:8000/docs`

---

## Аутентификация

В текущей версии API не требует аутентификации (MVP).

---

## Общие эндпоинты

### Health Check

```
GET /api/health
```

**Описание:** Проверка работоспособности сервера

**Ответ:**
```json
{
    "status": "ok",
    "service": "Android Agent Platform",
    "version": "1.0.0"
}
```

### Root

```
GET /
```

**Описание:** Корневой эндпоинт с информацией о сервере

**Ответ:**
```json
{
    "message": "Android Agent Platform API",
    "version": "1.0.0",
    "docs": "/docs",
    "health": "/api/health"
}
```

---

## Devices API (`/api/devices`)

Управление Android-устройствами через ADB и Tailscale VPN.

### GET /api/devices/

**Описание:** Получить список всех устройств с их статусами

**Ответ:**
```json
[
    {
        "id": "pixel-th-1",
        "name": "Pixel 5 - Thailand Device 1",
        "current_status": "online",
        "battery_level": 87,
        "temperature": 32.5,
        "memory_usage": 45,
        "active_tasks": 0,
        "last_heartbeat": "2025-12-04T10:30:00Z"
    }
]
```

**Статусы устройств:**
| Статус | Описание |
|--------|----------|
| `online` | Подключено и готово к работе |
| `offline` | Не доступно через ADB |
| `busy` | Выполняет задачу |
| `sleeping` | Период охлаждения |
| `overheating` | Температура >45°C |
| `low_battery` | Батарея <20% |

---

### GET /api/devices/{device_id}/status

**Описание:** Получить статус конкретного устройства (из кеша)

**Параметры:**
- `device_id` (path, string): ID устройства (например: "pixel-th-1")

**Ответ:** Объект DeviceStatus

**Ошибки:**
- `404` - Устройство не найдено

---

### POST /api/devices/{device_id}/refresh

**Описание:** Принудительное обновление статуса устройства (напрямую через ADB)

**Параметры:**
- `device_id` (path, string): ID устройства

**Ответ:** Обновленный DeviceStatus

**Время отклика:** 2-5 секунд

---

### POST /api/devices/{device_id}/reboot

**Описание:** Перезагрузка устройства через ADB

**Параметры:**
- `device_id` (path, string): ID устройства

**Ответ:**
```json
{
    "success": true,
    "message": "Device pixel-th-1 is rebooting",
    "device_id": "pixel-th-1"
}
```

**Время перезагрузки:** 60-90 секунд

---

### GET /api/devices/{device_id}/screenshot

**Описание:** Сделать скриншот экрана устройства

**Параметры:**
- `device_id` (path, string): ID устройства

**Ответ:**
```json
{
    "success": true,
    "device_id": "pixel-th-1",
    "screenshot_path": "/backend/data/screenshots/pixel-th-1/screenshot_20251204_103022.png"
}
```

---

### POST /api/devices/{device_id}/scrcpy

**Описание:** Запустить зеркалирование экрана через scrcpy

**Параметры:**
- `device_id` (path, string): ID устройства

**Ответ:**
```json
{
    "success": true,
    "message": "scrcpy launched for Pixel 5 - Thailand Device 1",
    "device_id": "pixel-th-1",
    "pid": 12345
}
```

**Требования:** scrcpy должен быть установлен на сервере

---

## Tasks API (`/api/tasks`)

Управление задачами отправки WhatsApp сообщений.

### POST /api/tasks/sync-notion

**Описание:** Синхронизация задач из Notion базы данных

**Параметры:**
- `limit` (query, int, default=10): Максимальное количество задач

**Ответ:**
```json
{
    "success": true,
    "tasks_synced": 5,
    "tasks": [...]
}
```

---

### POST /api/tasks/run

**Описание:** Запустить выполнение WhatsApp задачи

**Параметры:**
- `task_id` (query, string, optional): ID конкретной задачи. Если не указано - берется следующая по приоритету

**Процесс выполнения:**
1. Получение задачи из БД
2. Выбор устройства (Auto или конкретное)
3. Обновление статуса на "Running"
4. Открытие WhatsApp на устройстве
5. Поиск контакта по номеру
6. Ввод сообщения с имитацией человека
7. Отправка сообщения
8. Обновление Notion
9. Telegram уведомление

**Ответ (успех):**
```json
{
    "success": true,
    "task_id": "123",
    "status": "Sent",
    "device_id": "pixel-th-1",
    "duration_seconds": 45.2
}
```

**Ответ (ошибка):**
```json
{
    "success": false,
    "task_id": "123",
    "status": "Failed",
    "error": "Contact not found"
}
```

**Ошибки:**
- `404` - Задача не найдена / Нет pending задач
- `400` - Задача уже выполняется
- `503` - Нет доступных устройств

---

### GET /api/tasks/

**Описание:** Получить список задач с фильтрацией

**Параметры:**
- `status` (query, string, optional): Фильтр по статусу (Pending, Running, Sent, Failed)
- `device_id` (query, string, optional): Фильтр по устройству
- `limit` (query, int, default=50): Лимит результатов

**Ответ:** Массив TaskResponse объектов

---

### GET /api/tasks/{task_id}

**Описание:** Получить детали задачи по ID

**Ответ:** TaskResponse объект

**Ошибки:**
- `404` - Задача не найдена

---

### DELETE /api/tasks/{task_id}

**Описание:** Удалить задачу

**Ответ:**
```json
{
    "success": true,
    "message": "Task 123 deleted"
}
```

---

## Logs API (`/api/logs`)

Просмотр и управление логами действий.

### GET /api/logs/

**Описание:** Получить логи с фильтрацией

**Параметры:**
- `device_id` (query, string, optional): Фильтр по устройству
- `task_id` (query, string, optional): Фильтр по задаче
- `status` (query, string, optional): success/warning/failed/info
- `action_type` (query, string, optional): whatsapp_send/device_check/screenshot и т.д.
- `hours` (query, int, default=24): Временной диапазон в часах
- `limit` (query, int, default=100): Лимит результатов

**Ответ:**
```json
[
    {
        "id": 1234,
        "timestamp": "2025-12-04T10:30:15Z",
        "device_id": "pixel-th-1",
        "task_id": "123",
        "action": "whatsapp_send",
        "status": "success",
        "duration_seconds": 45.2,
        "error_message": null,
        "screenshot_path": "/path/to/screenshot.png"
    }
]
```

---

### GET /api/logs/{log_id}

**Описание:** Получить детали конкретного лога

**Ошибки:**
- `404` - Лог не найден

---

### GET /api/logs/stats/summary

**Описание:** Получить агрегированную статистику логов

**Параметры:**
- `device_id` (query, string, optional): Фильтр по устройству
- `hours` (query, int, default=24): Временной диапазон

**Ответ:**
```json
{
    "time_range_hours": 24,
    "total_logs": 156,
    "success_count": 142,
    "warning_count": 8,
    "failed_count": 6,
    "success_rate": 91.03,
    "action_counts": {
        "whatsapp_send": 120,
        "device_check": 24,
        "screenshot": 8
    },
    "device_id": null
}
```

---

### DELETE /api/logs/cleanup

**Описание:** Удалить старые логи

**Параметры:**
- `days` (query, int, default=30): Удалить логи старше N дней

**Ответ:**
```json
{
    "success": true,
    "deleted_count": 1547,
    "threshold_days": 30
}
```

---

## Scenarios API (`/api/scenarios`)

Управление сценариями автоматизации.

### GET /api/scenarios/

**Описание:** Список всех сценариев

**Параметры:**
- `status` (query, string, optional): Фильтр по статусу
- `device_id` (query, string, optional): Фильтр по устройству
- `limit` (query, int, default=50): Лимит
- `offset` (query, int, default=0): Смещение для пагинации

**Статусы сценариев:**
| Статус | Описание |
|--------|----------|
| `draft` | Черновик |
| `pending` | Запланирован |
| `running` | Выполняется |
| `paused` | На паузе |
| `completed` | Завершен |
| `failed` | Ошибка |
| `cancelled` | Отменен |

---

### POST /api/scenarios/

**Описание:** Создать новый сценарий

**Тело запроса:**
```json
{
    "name": "Morning WhatsApp Campaign",
    "description": "Утренняя рассылка приветствий",
    "device_id": "pixel-th-1",
    "priority": 5,
    "cron_expression": "0 9 * * *",
    "steps": [
        {
            "name": "Open WhatsApp",
            "agent_type": "whatsapp",
            "action": "open_app",
            "order": 1,
            "delay_before_seconds": 5
        },
        {
            "name": "Send Message",
            "agent_type": "whatsapp",
            "action": "send_message",
            "order": 2,
            "config": {
                "recipient": "+66812345678",
                "message": "Good morning!"
            }
        }
    ]
}
```

**Ответ:** Созданный ScenarioResponse

---

### GET /api/scenarios/{scenario_id}

**Описание:** Получить детали сценария со всеми шагами

---

### PUT /api/scenarios/{scenario_id}

**Описание:** Обновить сценарий (нельзя обновлять во время выполнения)

**Ошибки:**
- `400` - Cannot update a running scenario

---

### DELETE /api/scenarios/{scenario_id}

**Описание:** Удалить сценарий и все его шаги

---

### POST /api/scenarios/{scenario_id}/run

**Описание:** Запустить выполнение сценария

**Тело запроса (опционально):**
```json
{
    "device_id": "pixel-th-2",
    "skip_to_step": 3,
    "dry_run": false
}
```

**WebSocket события:**
- `scenario_started`
- `step_started`
- `step_completed`
- `step_failed`
- `scenario_completed`

---

### POST /api/scenarios/{scenario_id}/pause

**Описание:** Поставить сценарий на паузу

---

### POST /api/scenarios/{scenario_id}/resume

**Описание:** Продолжить выполнение сценария

---

### POST /api/scenarios/{scenario_id}/cancel

**Описание:** Отменить выполнение сценария

---

### GET /api/scenarios/{scenario_id}/steps

**Описание:** Получить все шаги сценария

---

### POST /api/scenarios/{scenario_id}/steps

**Описание:** Добавить шаг к сценарию

---

### PUT /api/scenarios/{scenario_id}/steps/{step_id}

**Описание:** Обновить шаг сценария

---

### DELETE /api/scenarios/{scenario_id}/steps/{step_id}

**Описание:** Удалить шаг из сценария

---

### POST /api/scenarios/{scenario_id}/schedule

**Описание:** Запланировать автоматическое выполнение

**Ответ:**
```json
{
    "success": true,
    "message": "Scenario scheduled",
    "next_run_at": "2025-12-05T09:00:00"
}
```

---

### DELETE /api/scenarios/{scenario_id}/schedule

**Описание:** Снять сценарий с расписания

---

### GET /api/scenarios/queue/status

**Описание:** Статус очереди и планировщика

**Ответ:**
```json
{
    "is_running": true,
    "active_jobs": 3,
    "queued_jobs": 5,
    "completed_today": 42,
    "failed_today": 2,
    "next_scheduled_job": {...}
}
```

---

### GET /api/scenarios/queue/items

**Описание:** Элементы в очереди

---

## Settings API (`/api/settings`)

Управление настройками приложения.

### GET /api/settings/

**Описание:** Получить все настройки (секреты маскируются)

**Ответ:**
```json
{
    "integrations": {
        "notion_api_key": "sec_...****",
        "notion_database_id": "abc1...****",
        "telegram_bot_token": "1234...****",
        "telegram_chat_id": "-1001234567890",
        "puter_api_key": "pk_...****",
        "puter_api_url": "https://api.puter.ai/v1",
        "puter_default_model": "claude-sonnet-4.5"
    },
    "behavior": {
        "min_typing_delay_ms": 50,
        "max_typing_delay_ms": 150,
        "min_action_delay_ms": 500,
        "max_action_delay_ms": 2000,
        "typo_probability": 0.03,
        "typo_fix_probability": 0.8,
        "max_messages_per_hour": 20,
        "max_messages_per_day": 100,
        "cooldown_after_batch_min": 30
    },
    "app": {
        "app_env": "development",
        "app_debug": true,
        "log_level": "INFO"
    }
}
```

---

### PUT /api/settings/integrations

**Описание:** Обновить настройки интеграций

**Тело запроса:**
```json
{
    "notion_api_key": "secret_xxx",
    "telegram_bot_token": "1234567890:ABC..."
}
```

---

### PUT /api/settings/behavior

**Описание:** Обновить настройки поведения

---

### PUT /api/settings/app

**Описание:** Обновить настройки приложения

---

### POST /api/settings/test/notion

**Описание:** Тест подключения к Notion

**Ответ (успех):**
```json
{
    "success": true,
    "message": "Connected to Notion successfully",
    "database_title": "WhatsApp Outreach"
}
```

---

### POST /api/settings/test/telegram

**Описание:** Тест Telegram бота (отправляет тестовое сообщение)

---

### GET /api/settings/status

**Описание:** Проверка конфигурации интеграций

**Ответ:**
```json
{
    "integrations": {
        "notion": {
            "configured": true,
            "api_key": true,
            "database_id": true
        },
        "telegram": {
            "configured": true,
            "bot_token": true,
            "chat_id": true
        },
        "puter": {
            "configured": false,
            "api_key": false
        }
    },
    "env_file_exists": true
}
```

---

## WebSocket API (`/ws`)

Real-time обновления через WebSocket.

### Подключение

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};
```

### Типы событий от сервера

| Тип события | Описание |
|------------|----------|
| `device_status_update` | Обновление статуса устройства |
| `task_started` | Задача начала выполнение |
| `task_progress` | Прогресс выполнения задачи |
| `task_completed` | Задача успешно завершена |
| `task_failed` | Задача завершилась с ошибкой |
| `scenario_started` | Сценарий начал выполнение |
| `step_started` | Шаг сценария начался |
| `step_completed` | Шаг сценария завершен |
| `step_failed` | Шаг сценария провалился |
| `scenario_completed` | Сценарий завершен |
| `log_entry` | Новая запись в логе |
| `notification` | Системное уведомление |

### Формат сообщения

```json
{
    "type": "task_progress",
    "timestamp": "2025-12-04T10:30:15Z",
    "payload": {
        "task_id": "123",
        "step": "typing_message",
        "progress": 65,
        "device_id": "pixel-th-1"
    }
}
```

### Пример: Подписка на обновления устройства

```javascript
ws.onmessage = (event) => {
    const { type, payload } = JSON.parse(event.data);

    if (type === 'device_status_update') {
        updateDeviceCard(payload.device_id, payload.status);
    }

    if (type === 'task_completed') {
        showToast(`Task ${payload.task_id} completed!`, 'success');
        refreshTasksList();
    }
};
```

---

## Коды ошибок

| Код | Описание |
|-----|----------|
| 400 | Bad Request - Неверные параметры |
| 404 | Not Found - Ресурс не найден |
| 500 | Internal Server Error - Ошибка сервера |
| 503 | Service Unavailable - Нет доступных устройств |

### Формат ошибки

```json
{
    "detail": "Error message",
    "error_code": "ERROR_CODE",
    "timestamp": "2025-12-04T10:30:15Z"
}
```

---

## Rate Limits

В текущей версии (MVP) rate limiting не реализован.

**Рекомендации:**
- Не более 20 сообщений в час на устройство
- Не более 100 сообщений в день на устройство
- Cooldown 30 минут после пакета сообщений

---

## Следующий документ

[FUNCTIONALITY.md](./05_FUNCTIONALITY.md) - Описание функциональности и что работает/не работает
