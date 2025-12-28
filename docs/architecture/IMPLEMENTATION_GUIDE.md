# IMPLEMENTATION_GUIDE.md — Полное руководство разработки

## РАЗДЕЛЕНИЕ ОТВЕТСТВЕННОСТИ: Backend vs Frontend vs Device Management

---

## ЧАСТЬ 1: ИНИЦИАЛИЗАЦИЯ ПРОЕКТА

### 1.1 Структура папок

```
android-agent-platform/
├── backend/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app entry
│   │   ├── config.py                # Configuration
│   │   ├── device_manager/
│   │   │   ├── __init__.py
│   │   │   ├── manager.py           # DeviceManager класс
│   │   │   ├── adb_handler.py       # ADB commands
│   │   │   ├── health_monitor.py    # Device health checks
│   │   │   └── models.py            # Device data models
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── base_agent.py        # BaseAgent класс
│   │   │   ├── whatsapp_agent.py    # WhatsApp логика
│   │   │   ├── linkedin_agent.py    # LinkedIn логика (future)
│   │   │   ├── instagram_agent.py   # Instagram логика (future)
│   │   │   └── recovery_agent.py    # Error recovery
│   │   ├── behaviors/
│   │   │   ├── __init__.py
│   │   │   ├── human_typing.py      # Эмуляция печати
│   │   │   ├── human_timing.py      # Эмуляция времени
│   │   │   ├── human_gestures.py    # Свайпы, клики
│   │   │   └── ui_analyzer.py       # Анализ скриншотов
│   │   ├── integrations/
│   │   │   ├── __init__.py
│   │   │   ├── notion_client.py     # Notion API
│   │   │   ├── telegram_bot.py      # Telegram Bot API
│   │   │   ├── llm_client.py        # Gemini API
│   │   │   └── ai_handler.py        # LLM logic wrapper
│   │   ├── orchestration/
│   │   │   ├── __init__.py
│   │   │   ├── task_scheduler.py    # Task scheduling
│   │   │   ├── scenario_runner.py   # Scenario execution
│   │   │   └── queue_manager.py     # Task queue
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── db.py                # SQLAlchemy setup
│   │   │   ├── models.py            # ORM models
│   │   │   ├── crud.py              # Database operations
│   │   │   └── schemas.py           # Pydantic schemas
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── devices.py           # /api/devices endpoints
│   │   │   ├── scenarios.py         # /api/scenarios endpoints
│   │   │   ├── tasks.py             # /api/tasks endpoints
│   │   │   ├── logs.py              # /api/logs endpoints
│   │   │   └── analytics.py         # /api/analytics endpoints
│   │   ├── websocket/
│   │   │   ├── __init__.py
│   │   │   └── manager.py           # WebSocket real-time updates
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── logger.py            # Logging configuration
│   │   │   ├── validators.py        # Input validation
│   │   │   └── helpers.py           # Helper functions
│   │   └── errors/
│   │       ├── __init__.py
│   │       └── exceptions.py        # Custom exceptions
│   ├── tests/
│   │   ├── unit/
│   │   │   ├── test_device_manager.py
│   │   │   ├── test_whatsapp_agent.py
│   │   │   └── test_human_typing.py
│   │   └── integration/
│   │       ├── test_full_workflow.py
│   │       └── test_notion_sync.py
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── Dockerfile
│   ├── .env.example
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── DevicePanel.tsx
│   │   │   ├── ScenarioBuilder.tsx
│   │   │   ├── LogsViewer.tsx
│   │   │   ├── Analytics.tsx
│   │   │   ├── Notifications.tsx
│   │   │   └── common/
│   │   │       ├── Button.tsx
│   │   │       ├── Card.tsx
│   │   │       ├── Modal.tsx
│   │   │       ├── Sidebar.tsx
│   │   │       └── ProgressBar.tsx
│   │   ├── pages/
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── ScenariosPage.tsx
│   │   │   ├── DevicesPage.tsx
│   │   │   └── LogsPage.tsx
│   │   ├── hooks/
│   │   │   ├── useApi.ts
│   │   │   ├── useWebSocket.ts
│   │   │   ├── useDeviceStatus.ts
│   │   │   └── useNotifications.ts
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   ├── websocket.ts
│   │   │   └── localStorage.ts
│   │   ├── types/
│   │   │   ├── device.ts
│   │   │   ├── task.ts
│   │   │   ├── scenario.ts
│   │   │   └── api.ts
│   │   ├── styles/
│   │   │   ├── theme.ts              # Твоя дизайн-система
│   │   │   ├── global.css
│   │   │   ├── components.css
│   │   │   └── animations.css
│   │   ├── utils/
│   │   │   ├── formatters.ts
│   │   │   ├── date-utils.ts
│   │   │   └── validators.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── public/
│   │   └── favicon.ico
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   └── README.md
│
├── scripts/
│   ├── init_db.py
│   ├── setup_pixel.sh           # Setup script for Pixel devices
│   ├── backup_db.py
│   └── test_connection.py
│
├── docs/
│   ├── API.md
│   ├── ARCHITECTURE.md
│   ├── DATABASE_SCHEMA.md
│   └── DEPLOYMENT.md
│
├── config/
│   ├── .env.example
│   └── default_settings.yaml
│
├── docker-compose.yml
├── .gitignore
├── README.md
└── CONTRIBUTING.md
```

### 1.2 Установка и первый запуск

**На ПК:**

```bash
# 1. Клонирование/инициализация
git clone <repository>
cd android-agent-platform

# 2. Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Backend зависимости
cd backend
pip install -r requirements.txt
cd ..

# 4. Frontend зависимости
cd frontend
npm install
cd ..

# 5. Environment setup
cp backend/config/.env.example backend/.env
# Заполнить: NOTION_API_KEY, TELEGRAM_BOT_TOKEN, GEMINI_API_KEY

# 6. База данных
python backend/scripts/init_db.py

# 7. Запуск backend
cd backend
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# 8. В другом терминале: frontend
cd frontend
npm run dev

# 9. Открыть http://localhost:3000
```

---

## ЧАСТЬ 2: BACKEND РАЗРАБОТКА (Python 3.11+)

### 2.1 Main entry point

**backend/src/main.py**

```python
# Инициализирует FastAPI приложение
# Подключает все роуты
# Запускает WebSocket manager
# Инициализирует Device Manager
# Инициализирует Task Scheduler
# Обрабатывает graceful shutdown
```

Ключевые функции:
- `create_app()` — создание FastAPI app
- `setup_routes()` — регистрация всех API endpoints
- `startup_events()` — инициализация при старте
- `shutdown_events()` — очистка при выключении
- `middleware` — логирование, CORS, error handling

### 2.2 DeviceManager (src/device_manager/)

**Что это делает:**
- Подключается к каждому Pixel через ADB over Tailscale
- Проверяет статус (online/offline) каждые 60 сек
- Мониторит батарею, температуру, память
- Обновляет UI в реальном времени
- Автоматически перезагружает девайс если проблемы

**Основные классы:**

```python
class DeviceManager:
    """Главный менеджер устройств"""
    
    def __init__(self):
        self.devices = {
            'pixel-th-1': Device(...),
            'pixel-vn-1': Device(...),
            'pixel-th-2': Device(...)
        }
        self.health_monitor = HealthMonitor()
    
    async def initialize(self):
        """Инициализирует все устройства"""
        for device in self.devices.values():
            await device.connect()
        
        # Стартует фоновый мониторинг
        asyncio.create_task(self.health_monitor.run_continuously())
    
    async def get_device_status(self, device_id: str) -> DeviceStatus:
        """Возвращает статус конкретного девайса"""
        device = self.devices[device_id]
        return DeviceStatus(
            online=await device.is_online(),
            battery=await device.get_battery(),
            temperature=await device.get_temperature(),
            ram_usage=await device.get_ram_usage(),
            signal_strength=await device.get_signal_strength()
        )
    
    async def execute_adb_command(self, device_id: str, cmd: str) -> str:
        """Выполняет ADB команду на девайсе"""
        device = self.devices[device_id]
        return await device.execute(cmd)
    
    async def take_screenshot(self, device_id: str) -> bytes:
        """Берёт скриншот"""
        device = self.devices[device_id]
        return await device.take_screenshot()
    
    async def monitor_health(self):
        """Бесконечный цикл мониторинга"""
        while True:
            for device_id, device in self.devices.items():
                status = await self.get_device_status(device_id)
                
                # Проверка критических значений
                if status.temperature > 40:
                    await self.notify_warning(f"{device_id}: High temperature")
                if status.battery < 15:
                    await self.notify_warning(f"{device_id}: Low battery")
                
                # Отправить в WebSocket для реального обновления UI
                await websocket_manager.broadcast({
                    'type': 'device_status_update',
                    'device_id': device_id,
                    'status': status.dict()
                })
            
            await asyncio.sleep(60)  # Проверка каждые 60 сек

class Device:
    """Представление одного физического девайса"""
    
    async def connect(self):
        """Подключение через ADB"""
        # adb connect pixel-th-1:5555
        pass
    
    async def is_online(self) -> bool:
        """Проверка онлайн статуса"""
        pass
    
    async def execute(self, cmd: str) -> str:
        """Выполнить ADB команду"""
        pass

class HealthMonitor:
    """Фоновый мониторинг здоровья устройств"""
    
    async def run_continuously(self):
        """Бежит непрерывно, проверяет статус"""
        pass
```

### 2.3 Behavior Layer (src/behaviors/)

**Эмуляция человеческого поведения — это КРИТИЧНО**

**human_typing.py**

```python
class HumanTyping:
    """Печатает текст как человек (не робот)"""
    
    @staticmethod
    async def type_text(device, text: str, add_typos: bool = False):
        """
        Печатает текст медленно с естественными паузами
        
        Параметры:
        - average_speed: ~80 chars per minute (как человек)
        - inter_char_delay: Gaussian distribution, не uniform
        - pause_points: иногда останавливается посередине слова
        - typo_rate: иногда неправильный символ + backspace + исправление
        """
        words = text.split(' ')
        
        for i, word in enumerate(words):
            for j, char in enumerate(word):
                # Базовая задержка между символами
                base_delay = random.gauss(0.08, 0.03)  # ms, Gaussian
                
                # Иногда ошибка
                if add_typos and random.random() < 0.05:  # 5% ошибок
                    wrong_char = chr(ord(char) + random.randint(-1, 1))
                    await device.tap_key(wrong_char)
                    await asyncio.sleep(random.uniform(0.2, 0.5))
                    await device.tap_key('BACKSPACE')
                    await asyncio.sleep(random.uniform(0.1, 0.3))
                
                # Печать правильного символа
                await device.tap_key(char)
                
                # Пауза
                await asyncio.sleep(base_delay)
                
                # Иногда длинная пауза (человек думает)
                if random.random() < 0.02:  # 2% шанса
                    await asyncio.sleep(random.uniform(1.0, 3.0))
            
            # Пробел между словами
            if i < len(words) - 1:
                await device.tap_key('SPACE')
                await asyncio.sleep(random.gauss(0.1, 0.05))

class HumanTiming:
    """Эмулирует естественный ритм действий"""
    
    @staticmethod
    def get_random_delay(min_sec: float, max_sec: float) -> float:
        """
        Возвращает рандомную задержку с Gaussian distribution
        Не uniform, чтобы выглядело естественнее
        """
        mean = (min_sec + max_sec) / 2
        std_dev = (max_sec - min_sec) / 4
        value = random.gauss(mean, std_dev)
        return max(min_sec, min(max_sec, value))
    
    @staticmethod
    def should_be_active_now(timezone: str, account_age_days: int) -> bool:
        """
        Определяет должен ли агент быть активным СЕЙЧАС
        
        Учитывает:
        - Локальное время устройства (не UTC)
        - День недели (сб-вс активность ниже)
        - Возраст аккаунта (первая неделя: максимум 5 сообщений/день)
        - Перерывы (каждые 3-4 часа пауза)
        """
        current_time = datetime.now(pytz.timezone(timezone))
        hour = current_time.hour
        day_of_week = current_time.weekday()
        
        # Основное окно активности: 08:00-22:00
        if hour < 8 or hour >= 22:
            return False
        
        # Выходные дни: сниженная активность
        if day_of_week >= 5:  # Сб-Вс
            return random.random() < 0.5  # 50% шанс
        
        # Новые аккаунты: максимум 5 сообщений в день
        if account_age_days < 7:
            # Распределить 5 сообщений по 14 часам
            return random.random() < (5 / 14)
        
        return True

class HumanGestures:
    """Эмулирует свайпы, клики, скроллы"""
    
    @staticmethod
    async def tap(device, x: int, y: int):
        """
        Клик как человек: микро-пауза перед кликом
        """
        pre_delay = random.uniform(0.05, 0.2)
        await asyncio.sleep(pre_delay)
        await device.tap(x, y)
        post_delay = random.uniform(0.2, 0.5)
        await asyncio.sleep(post_delay)
    
    @staticmethod
    async def swipe(device, x1: int, y1: int, x2: int, y2: int):
        """
        Свайп не ровный, а с ускорением/замедлением
        """
        duration = random.uniform(0.5, 1.2)  # сек
        await device.swipe(x1, y1, x2, y2, duration)
```

### 2.4 AI Agents (src/agents/)

**BaseAgent — базовый класс для всех агентов**

```python
class BaseAgent:
    """Базовый класс для WhatsApp, LinkedIn, Instagram агентов"""
    
    def __init__(self, device_manager, llm_client, notion_client):
        self.device = device_manager
        self.llm = llm_client
        self.notion = notion_client
    
    async def execute_task(self, task: Task) -> TaskResult:
        """
        Главный метод выполнения задачи
        
        1. Планирование (LLM)
        2. Выполнение шагов
        3. Валидация
        4. Логирование
        """
        try:
            # 1. Plan
            steps = await self.plan_task(task)
            
            # 2. Execute each step
            for step in steps:
                result = await self.execute_step(step)
                if not result.success:
                    # Recovery logic
                    recovery_result = await self.recover_from_error(step, result.error)
                    if not recovery_result.success:
                        raise Exception(f"Step failed: {step}")
            
            # 3. Validate
            await self.validate_completion(task)
            
            # 4. Log
            return TaskResult(success=True)
        
        except Exception as e:
            return TaskResult(success=False, error=str(e))
    
    async def plan_task(self, task: Task) -> List[Step]:
        """LLM планирует шаги"""
        prompt = f"""
        Task: {task.description}
        Context: {task.context}
        
        Create a step-by-step plan for this task.
        Return as JSON list of steps.
        """
        response = await self.llm.generate(prompt)
        return json.loads(response)
    
    async def execute_step(self, step: Step):
        """Выполняет один шаг"""
        # Переопределяется в подклассах
        pass
    
    async def recover_from_error(self, step: Step, error: str):
        """Восстанавливается от ошибок"""
        # Уровни восстановления описаны в IDEAL_VISION.md
        pass
    
    async def take_smart_screenshot(self) -> Image:
        """
        Берёт скриншот ТОЛЬКО когда нужно
        (не для каждого действия)
        """
        pass

class WhatsAppAgent(BaseAgent):
    """Отправляет WhatsApp сообщения"""
    
    async def send_message(self, phone: str, text: str) -> bool:
        """
        Отправить одно сообщение
        
        Процесс:
        1. Открыть WhatsApp
        2. Найти контакт
        3. Ввести сообщение с human_typing
        4. Отправить
        5. Валидировать через скриншот
        """
        
        # 1. Open WhatsApp
        await self.device.tap_app('com.whatsapp')
        await asyncio.sleep(HumanTiming.get_random_delay(2, 4))
        
        # 2. Find contact
        contact_found = await self.find_contact(phone)
        if not contact_found:
            return False  # Контакт не найден
        
        # 3. Type message
        await HumanTyping.type_text(self.device, text, add_typos=True)
        await asyncio.sleep(HumanTiming.get_random_delay(1, 3))
        
        # 4. Send
        await self.device.tap_send_button()
        await asyncio.sleep(HumanTiming.get_random_delay(2, 5))
        
        # 5. Validate
        screenshot = await self.device.take_screenshot()
        is_sent = await self.validate_message_sent(screenshot)
        
        return is_sent
    
    async def find_contact(self, phone: str) -> bool:
        """Находит контакт по номеру телефона"""
        # Использовать XML parsing, не скриншоты
        # быстрее и надёжнее
        pass
    
    async def validate_message_sent(self, screenshot: bytes) -> bool:
        """Проверяет что сообщение отправилось"""
        # LLM анализирует скриншот
        # "Is message marked as sent/delivered?"
        pass
    
    async def send_batch(self, messages: List[dict]) -> dict:
        """Отправить несколько сообщений подряд"""
        results = {
            'success': 0,
            'failed': 0,
            'errors': []
        }
        
        for msg in messages:
            success = await self.send_message(msg['phone'], msg['text'])
            if success:
                results['success'] += 1
            else:
                results['failed'] += 1
                results['errors'].append(msg['phone'])
            
            # Пауза между сообщениями
            interval = HumanTiming.get_random_delay(15*60, 25*60)  # 15-25 минут
            await asyncio.sleep(interval)
        
        return results
```

### 2.5 Integration Layer (src/integrations/)

**notion_client.py**

```python
class NotionClient:
    """Работает с Notion базой"""
    
    async def get_pending_tasks(self, limit: int = 10) -> List[dict]:
        """
        Получить Pending задачи из Notion
        Сортировать по приоритету
        """
        response = await self.client.query_database(
            database_id=self.db_id,
            filter={
                "property": "Status",
                "status": {"equals": "Pending"}
            },
            sorts=[
                {"property": "Priority", "direction": "descending"}
            ]
        )
        return response['results']
    
    async def update_task_status(self, task_id: str, status: str, notes: str = ""):
        """Обновить статус одной задачи"""
        # Единичный апдейт
        pass
    
    async def batch_update_tasks(self, updates: List[dict]):
        """
        Batch обновления (экономит API rate limits)
        
        updates = [
            {'task_id': '...', 'status': 'Sent', 'notes': 'msg delivered'},
            {'task_id': '...', 'status': 'Failed', 'notes': 'invalid number'},
        ]
        """
        # Группировать обновления
        # Отправить разом (max 10 за раз, чтобы не перегрузить)
        pass
```

**telegram_bot.py**

```python
class TelegramNotifier:
    """Отправляет уведомления в Telegram"""
    
    async def send_alert(self, level: str, message: str, action_buttons: dict = None):
        """
        level: 'info', 'warning', 'error'
        message: текст сообщения
        action_buttons: {'button_text': 'callback_id'}
        """
        
        emoji = {'info': 'ℹ️', 'warning': '⚠️', 'error': '❌'}[level]
        
        text = f"{emoji} {message}"
        
        # Отправить с кнопками если есть
        if action_buttons:
            await self.send_with_buttons(text, action_buttons)
        else:
            await self.send_text(text)
    
    async def ask_user_for_decision(self, question: str, options: List[str]):
        """
        Спросить пользователя через Telegram
        Вернуть выбранный вариант
        """
        message_id = await self.send_question(question, options)
        
        # Ждать ответ
        response = await self.wait_for_response(message_id, timeout=300)
        return response
```

**llm_client.py**

```python
class LLMClient:
    """Работает с Gemini 3 Pro API"""
    
    def __init__(self, api_key: str = None, proxy_url: str = None):
        """
        api_key: Gemini API key (если есть direct access)
        proxy_url: Proxy API endpoint (например, laozhang.ai)
        """
        self.api_key = api_key
        self.proxy_url = proxy_url
        self.client = self._init_client()
    
    async def generate_message(self, context: dict, template: str) -> str:
        """
        Генерирует персонализированное сообщение
        
        context = {
            'recipient_name': 'John',
            'recipient_category': 'prospect',
            'company': 'TechCorp',
            'previous_interaction': '2 weeks ago'
        }
        
        template = "professional_cold_outreach"
        """
        
        prompt = f"""
        Generate a WhatsApp message with this context:
        Name: {context['recipient_name']}
        Company: {context['company']}
        Category: {context['recipient_category']}
        
        Use template: {template}
        
        Message should be:
        - Personalized
        - 1-3 sentences max
        - Professional but friendly
        - No links
        
        Return ONLY the message text, nothing else.
        """
        
        response = await self.generate(prompt)
        return response.strip()
    
    async def analyze_screenshot(self, image: bytes, question: str) -> str:
        """
        Анализирует скриншот через LLM
        
        question = "Is the message sent successfully?"
        """
        
        response = await self.analyze_image(image, question)
        return response
    
    async def plan_task(self, task: dict) -> List[str]:
        """
        Создаёт план выполнения задачи
        """
        prompt = f"""
        Create a step-by-step plan for this task:
        {task}
        
        Return as numbered list (1. 2. 3. etc)
        Each step should be specific and actionable.
        """
        
        response = await self.generate(prompt)
        steps = [s.strip() for s in response.split('\n') if s.strip()]
        return steps
    
    async def generate(self, prompt: str) -> str:
        """Базовый метод генерации"""
        if self.proxy_url:
            return await self._call_proxy_api(prompt)
        else:
            return await self._call_gemini_direct(prompt)
    
    async def _call_proxy_api(self, prompt: str) -> str:
        """Если используется proxy (типа laozhang.ai)"""
        headers = {'Authorization': f'Bearer {self.api_key}'}
        data = {'prompt': prompt, 'model': 'gemini-3-pro'}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.proxy_url}/v1/chat/completions",
                json=data,
                headers=headers
            )
            return response.json()['choices'][0]['message']['content']
```

### 2.6 Task Orchestration (src/orchestration/)

**scenario_runner.py**

```python
class ScenarioRunner:
    """Выполняет сценарии (последовательность действий)"""
    
    async def run_scenario(self, scenario: Scenario) -> ScenarioResult:
        """
        Выполняет сценарий шаг за шагом
        
        scenario.steps = [
            Step(type='whatsapp', params={'messages': 10}),
            Step(type='wait', params={'minutes': 120}),
            Step(type='linkedin', params={'actions': 'like,follow'}),
        ]
        """
        
        result = ScenarioResult()
        
        for i, step in enumerate(scenario.steps):
            # Отправить прогресс в UI
            await self.notify_progress(step_index=i, total_steps=len(scenario.steps))
            
            # Выполнить шаг
            step_result = await self.execute_step(step)
            result.steps_results.append(step_result)
            
            if not step_result.success:
                # Проверить есть ли condition для recovery
                if step.has_recovery_condition:
                    recovery_result = await self.execute_recovery(step)
                    if not recovery_result.success:
                        result.success = False
                        break
                else:
                    result.success = False
                    break
        
        result.success = all(s.success for s in result.steps_results)
        return result
    
    async def execute_step(self, step: Step) -> StepResult:
        """Выполняет один шаг сценария"""
        
        if step.type == 'whatsapp':
            return await self.whatsapp_agent.send_batch(step.messages)
        
        elif step.type == 'wait':
            await asyncio.sleep(step.minutes * 60)
            return StepResult(success=True)
        
        elif step.type == 'linkedin':
            return await self.linkedin_agent.perform_activities(step.actions)
        
        elif step.type == 'instagram':
            return await self.instagram_agent.post_reel(step.video_source)
        
        elif step.type == 'recovery':
            return await self.execute_recovery(step)
```

### 2.7 Database Models (src/database/models.py)

**SQLAlchemy ORM models:**

```python
class Device(Base):
    __tablename__ = "devices"
    
    id = Column(String, primary_key=True)
    name = Column(String)
    device_id = Column(String, unique=True)
    location = Column(String)
    timezone = Column(String)
    last_heartbeat = Column(DateTime, default=datetime.utcnow)
    current_status = Column(String)
    battery_level = Column(Integer)
    temperature = Column(Float)
    memory_usage = Column(Integer)
    active_tasks = Column(Integer, default=0)

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True)
    notion_id = Column(String, unique=True)
    task_type = Column(String)  # 'whatsapp', 'linkedin', 'instagram'
    status = Column(String)  # 'pending', 'running', 'success', 'failed'
    device_id = Column(String, ForeignKey('devices.id'))
    content = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    attempt_count = Column(Integer, default=0)
    error_message = Column(String, nullable=True)

class Scenario(Base):
    __tablename__ = "scenarios"
    
    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String, nullable=True)
    steps = Column(JSON)  # Serialized steps
    enabled = Column(Boolean, default=True)
    schedule = Column(String, nullable=True)  # Cron expression
    created_at = Column(DateTime, default=datetime.utcnow)

class Log(Base):
    __tablename__ = "logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    device_id = Column(String, ForeignKey('devices.id'))
    task_id = Column(String, ForeignKey('tasks.id'), nullable=True)
    action = Column(String)
    status = Column(String)  # 'success', 'failed', 'warning'
    duration_seconds = Column(Float, nullable=True)
    error_message = Column(String, nullable=True)
    screenshot_path = Column(String, nullable=True)
    metadata = Column(JSON, nullable=True)
```

### 2.8 API Routes (src/routes/)

**devices.py**

```python
router = APIRouter(prefix="/api/devices", tags=["devices"])

@router.get("/")
async def get_all_devices():
    """Получить список всех Pixel'й"""
    devices = await device_manager.get_all_devices()
    return devices

@router.get("/{device_id}/status")
async def get_device_status(device_id: str):
    """Получить статус конкретного устройства"""
    status = await device_manager.get_device_status(device_id)
    return status

@router.post("/{device_id}/restart")
async def restart_device(device_id: str):
    """Перезагрузить устройство"""
    await device_manager.restart_device(device_id)
    return {"status": "restarting"}

@router.post("/{device_id}/clear-cache")
async def clear_cache(device_id: str):
    """Очистить кеш приложений"""
    await device_manager.clear_cache(device_id)
    return {"status": "cache cleared"}
```

**scenarios.py**

```python
router = APIRouter(prefix="/api/scenarios", tags=["scenarios"])

@router.post("/")
async def create_scenario(scenario: ScenarioCreate):
    """Создать новый сценарий"""
    scenario_obj = await db.create_scenario(scenario)
    return scenario_obj

@router.get("/")
async def list_scenarios():
    """Получить список всех сценариев"""
    return await db.list_scenarios()

@router.post("/{scenario_id}/run")
async def run_scenario(scenario_id: str):
    """Запустить сценарий сейчас"""
    result = await scenario_runner.run_scenario(scenario_id)
    return result

@router.post("/{scenario_id}/schedule")
async def schedule_scenario(scenario_id: str, schedule: str):
    """Расписание сценария (cron expression)"""
    await db.update_scenario_schedule(scenario_id, schedule)
    return {"status": "scheduled"}
```

---

## ЧАСТЬ 3: FRONTEND РАЗРАБОТКА (React + TypeScript)

### 3.1 Структура компонентов

Следовать 100% твоей дизайн-системе из V3-DESIGN_SYSTEM.md

**theme.ts — преобразование дизайн-системы в код**

```typescript
export const theme = {
  colors: {
    primary: "#008AFF",
    secondary: "#6B7280",
    success: "#10B981",
    error: "#EF4444",
    warning: "#F59E0B",
    background: "#FFFFFF",
    surface: "#F9FAFB",
    // ... остальные из V3-DESIGN_SYSTEM.md
  },
  typography: {
    fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    fontSize: {
      xs: "11px",
      sm: "12px",
      base: "14px",
      lg: "16px",
      xl: "18px",
      // ...
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
  },
  spacing: {
    0: "0",
    1: "4px",
    2: "8px",
    4: "16px",
    6: "24px",
    // ...
  },
  borderRadius: {
    sm: "6px",
    base: "8px",
    lg: "12px",
    full: "9999px",
  },
  shadows: {
    sm: "0 1px 2px rgba(0,0,0,0.05)",
    md: "0 4px 6px rgba(0,0,0,0.1)",
    lg: "0 10px 15px rgba(0,0,0,0.15)",
  },
};
```

### 3.2 Главные компоненты

**Dashboard.tsx**

```typescript
export const Dashboard: React.FC = () => {
  const [devices, setDevices] = useState<Device[]>([]);
  const [currentActivity, setCurrentActivity] = useState<Activity | null>(null);
  const [recentLogs, setRecentLogs] = useState<Log[]>([]);
  
  useEffect(() => {
    // Подключиться к WebSocket для real-time обновлений
    const ws = useWebSocket();
    
    ws.on('device_status_update', (data) => {
      setDevices(prev => 
        prev.map(d => d.id === data.device_id ? {...d, ...data.status} : d)
      );
    });
    
    ws.on('activity_update', (data) => {
      setCurrentActivity(data);
    });
    
    ws.on('log_entry', (data) => {
      setRecentLogs(prev => [data, ...prev].slice(0, 10));
    });
    
    return () => ws.close();
  }, []);
  
  return (
    <div style={{ display: 'flex', gap: theme.spacing[4] }}>
      {/* Device Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: theme.spacing[2] }}>
        {devices.map(device => (
          <DeviceCard key={device.id} device={device} />
        ))}
      </div>
      
      {/* Current Activity */}
      {currentActivity && (
        <CurrentActivityBlock activity={currentActivity} />
      )}
      
      {/* Recent Logs */}
      <RecentActivityLog logs={recentLogs} />
    </div>
  );
};
```

**ScenarioBuilder.tsx**

```typescript
export const ScenarioBuilder: React.FC = () => {
  const [steps, setSteps] = useState<Step[]>([]);
  const [scenarioName, setScenarioName] = useState('');
  
  const handleAddStep = (stepType: string) => {
    const newStep: Step = {
      id: generateId(),
      type: stepType,
      config: getDefaultConfig(stepType),
    };
    setSteps([...steps, newStep]);
  };
  
  const handleDragEnd = (result) => {
    const { source, destination } = result;
    if (!destination) return;
    
    const newSteps = Array.from(steps);
    const [removed] = newSteps.splice(source.index, 1);
    newSteps.splice(destination.index, 0, removed);
    setSteps(newSteps);
  };
  
  return (
    <div>
      {/* Available Actions Menu */}
      <div style={{ width: '200px', marginRight: theme.spacing[4] }}>
        <h3>Available Actions</h3>
        {AVAILABLE_ACTIONS.map(action => (
          <button
            key={action.id}
            onClick={() => handleAddStep(action.type)}
          >
            {action.icon} {action.label}
          </button>
        ))}
      </div>
      
      {/* Visual Constructor */}
      <DragDropContext onDragEnd={handleDragEnd}>
        <Droppable droppableId="scenario-steps">
          {(provided) => (
            <div ref={provided.innerRef} {...provided.droppableProps}>
              {steps.map((step, index) => (
                <Draggable key={step.id} draggableId={step.id} index={index}>
                  {(provided) => (
                    <div
                      ref={provided.innerRef}
                      {...provided.draggableProps}
                      {...provided.dragHandleProps}
                    >
                      <StepCard step={step} />
                    </div>
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
            </div>
          )}
        </Droppable>
      </DragDropContext>
      
      {/* Save Button */}
      <button
        onClick={() => saveScenario(scenarioName, steps)}
      >
        Save Scenario
      </button>
    </div>
  );
};
```

### 3.3 Real-time WebSocket Integration

**useWebSocket.ts**

```typescript
export const useWebSocket = () => {
  const [ws, setWs] = useState<WebSocket | null>(null);
  
  useEffect(() => {
    const websocket = new WebSocket('ws://localhost:8000/ws');
    
    websocket.onopen = () => {
      console.log('WebSocket connected');
    };
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      // Dispatch событию (или использовать callback)
      window.dispatchEvent(new CustomEvent('ws-message', { detail: data }));
    };
    
    setWs(websocket);
    
    return () => websocket.close();
  }, []);
  
  return {
    send: (data) => ws?.send(JSON.stringify(data)),
    on: (event, handler) => {
      window.addEventListener('ws-message', (e: any) => {
        if (e.detail.type === event) {
          handler(e.detail);
        }
      });
    },
  };
};
```

### 3.4 Icons Integration

**Boxicons для обычных иконок:**
```bash
npm install boxicons
```

```typescript
import { BiCog, BiHome, BiListUl } from 'react-icons/bi';

<BiCog size={24} color={theme.colors.primary} />
```

**Simple Icons для соц сетей:**
```bash
npm install simple-icons
```

```typescript
import * as SI from 'simple-icons';

const whatsappIcon = SI.siWhatsapp;
const linkedinIcon = SI.siLinkedin;
```

---

## ЧАСТЬ 4: ИНТЕГРАЦИЯ И ТЕСТИРОВАНИЕ

### 4.1 Unit Tests

**tests/unit/test_whatsapp_agent.py**

```python
import pytest
from src.agents.whatsapp_agent import WhatsAppAgent

@pytest.mark.asyncio
async def test_send_message_success():
    """Тест успешной отправки сообщения"""
    agent = WhatsAppAgent(mock_device, mock_llm, mock_notion)
    
    result = await agent.send_message("+66812345678", "Hello!")
    
    assert result == True

@pytest.mark.asyncio
async def test_send_message_invalid_number():
    """Тест отправки на неправильный номер"""
    agent = WhatsAppAgent(mock_device, mock_llm, mock_notion)
    
    result = await agent.send_message("+invalid", "Hello!")
    
    assert result == False
```

### 4.2 Integration Tests

**tests/integration/test_full_workflow.py**

```python
@pytest.mark.asyncio
async def test_full_scenario_execution():
    """Полный тест выполнения сценария"""
    
    # 1. Create scenario
    scenario = await scenario_runner.create_scenario({
        'name': 'Test WhatsApp',
        'steps': [
            {'type': 'whatsapp', 'messages': [
                {'phone': '+66812345678', 'text': 'Test message 1'},
            ]}
        ]
    })
    
    # 2. Run scenario
    result = await scenario_runner.run_scenario(scenario)
    
    # 3. Assert
    assert result.success == True
    assert len(result.steps_results) == 1
```

### 4.3 Deployment

**docker-compose.yml**

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      NOTION_API_KEY: ${NOTION_API_KEY}
      TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN}
      GEMINI_API_KEY: ${GEMINI_API_KEY}
    volumes:
      - ./backend/data:/app/data
    depends_on:
      - db
  
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      VITE_API_URL: http://backend:8000
  
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## ИТОГОВЫЙ ЧЕК-ЛИСТ

Перед запуском:
- [ ] Python 3.11+ установлен
- [ ] Node.js 18+ установлен
- [ ] .env файл заполнен
- [ ] Все 3 Pixel'я подключены через ADB
- [ ] Backend запущен (localhost:8000)
- [ ] Frontend запущен (localhost:3000)
- [ ] Notion таблица создана и API ключ работает
- [ ] Telegram бот создан и токен работает
- [ ] Gemini API key работает (или proxy сервис настроен)
- [ ] WebSocket соединение работает
- [ ] Первый тестовый сценарий успешно выполнен

Если всё ✅ — система готова к использованию!
