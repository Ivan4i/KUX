# REMOTE_CONTROL_AND_AUTOMATION.md — Полная спецификация удаленного управления и Android UI автоматизации

## ⚠️ КРИТИЧНЫЙ ФАЙЛ — ВНИМАНИЕ CLAUDE

Этот файл содержит ОБЯЗАТЕЛЬНЫЕ дополнения к архитектуре. Claude ДОЛЖЕН реализовать всё, что здесь описано, в первой версии приложения.

---

## ЧАСТЬ 1: SCRCPY ИНТЕГРАЦИЯ (Remote Visual Control)

### 1.1 Что это

**Scrcpy** — это инструмент, который:
- Стримит видео с экрана Android устройства на ПК через ADB (низкая задержка, высокая скорость)
- Позволяет управлять сенсорным экраном мышкой и клавиатурой с ПК
- Работает полностью локально через ADB (не нужен интернет, не нужны облачные сервисы)

**Зачем это нужно:**
- Если агент "застрял" — ты можешь вмешаться вручную и "подправить" что-то
- Если нужно отладить поведение агента — видишь, что происходит на экране
- Если случился непредвиденный UI-элемент — можешь сам нажать кнопку и помочь боту продолжить

### 1.2 Установка Scrcpy

**Windows:**
```bash
choco install scrcpy
# Или скачать ZIP с https://github.com/Genymobile/scrcpy/releases
```

**macOS:**
```bash
brew install scrcpy
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install scrcpy
```

**Проверка установки:**
```bash
scrcpy --version
# Должен вывести версию
```

### 1.3 Запуск из приложения (Backend)

**backend/src/device_manager/remote_control.py** (новый файл)

```python
import subprocess
import os
import platform
from typing import Optional

class RemoteControlManager:
    """Управляет сеансами удаленного доступа через scrcpy"""
    
    def __init__(self):
        self.active_sessions = {}  # device_id -> process
        self.scrcpy_path = self._find_scrcpy()
        
        if not self.scrcpy_path:
            raise RuntimeError("scrcpy not found. Install it first.")
    
    def _find_scrcpy(self) -> Optional[str]:
        """Находит путь к scrcpy исполняемому файлу"""
        # Windows
        if platform.system() == "Windows":
            result = os.popen("where scrcpy").read().strip()
            return result if result else None
        
        # Mac/Linux
        result = os.popen("which scrcpy").read().strip()
        return result if result else None
    
    def start_remote_session(self, device_serial: str, device_id: str) -> dict:
        """
        Запускает окно scrcpy для конкретного устройства
        
        Параметры:
        - device_serial: 'pixel-th-1:5555' (ADB serial, с портом)
        - device_id: 'pixel-th-1' (для отслеживания сеанса)
        
        Возвращает:
        {
            'status': 'success' | 'error',
            'session_id': 'unique_id',
            'message': 'описание'
        }
        """
        
        try:
            # Если сеанс для этого девайса уже открыт, закрыть его
            if device_id in self.active_sessions:
                self.stop_remote_session(device_id)
            
            # Параметры scrcpy
            cmd = [
                self.scrcpy_path,
                "--serial", device_serial,
                "--max-size", "1024",              # Разрешение для производительности
                "--video-bit-rate", "4M",          # Битрейт для стабильности через VPN
                "--window-title", f"Remote: {device_id}",
                "--stay-awake",                     # Экран не засыпает
                "--show-touches",                   # Показывать касания (для отладки)
            ]
            
            # Запуск процесса (не блокирует основной процесс)
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if platform.system() == "Windows" else 0
            )
            
            # Сохранить процесс в памяти
            self.active_sessions[device_id] = process
            
            return {
                'status': 'success',
                'session_id': device_id,
                'message': f'Remote control window opened for {device_id}. You can now control the device with mouse and keyboard.',
                'pid': process.pid
            }
        
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to start remote session: {str(e)}'
            }
    
    def stop_remote_session(self, device_id: str) -> dict:
        """Закрывает окно scrcpy"""
        if device_id not in self.active_sessions:
            return {'status': 'warning', 'message': 'No active session for this device'}
        
        try:
            process = self.active_sessions[device_id]
            process.terminate()
            process.wait(timeout=5)
            del self.active_sessions[device_id]
            
            return {'status': 'success', 'message': 'Remote session closed'}
        
        except subprocess.TimeoutExpired:
            process.kill()
            del self.active_sessions[device_id]
            return {'status': 'success', 'message': 'Remote session force-closed'}
        
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def list_active_sessions(self) -> list:
        """Список открытых сеансов"""
        return list(self.active_sessions.keys())
    
    def is_session_active(self, device_id: str) -> bool:
        """Проверить активен ли сеанс"""
        if device_id not in self.active_sessions:
            return False
        
        process = self.active_sessions[device_id]
        return process.poll() is None  # poll() returns None если процесс еще живой
```

**backend/src/device_manager/manager.py** (добавить в DeviceManager)

```python
from .remote_control import RemoteControlManager

class DeviceManager:
    def __init__(self):
        # ... существующий код ...
        self.remote_control = RemoteControlManager()
    
    async def start_remote_control(self, device_id: str) -> dict:
        """
        Запустить удаленное управление этим устройством
        
        ВАЖНО: Ставит агента на паузу, если он работает!
        """
        device = self.devices.get(device_id)
        if not device:
            return {'status': 'error', 'message': f'Device {device_id} not found'}
        
        # Ставим агента на паузу (если работает)
        await self.pause_device_tasks(device_id)
        
        # Запускаем scrcpy
        result = self.remote_control.start_remote_session(
            device_serial=device.adb_serial,  # 'pixel-th-1:5555'
            device_id=device_id
        )
        
        return result
    
    async def stop_remote_control(self, device_id: str) -> dict:
        """Закрыть удаленное управление"""
        return self.remote_control.stop_remote_session(device_id)
    
    async def pause_device_tasks(self, device_id: str):
        """Поставить все задачи на паузу для этого девайса"""
        # Интеграция с task_scheduler
        # await self.task_scheduler.pause_device(device_id)
        pass
```

### 1.4 API Endpoints (backend/src/routes/devices.py)

```python
from fastapi import APIRouter

router = APIRouter(prefix="/api/devices", tags=["devices"])

@router.post("/{device_id}/remote-control/start")
async def start_remote_control(device_id: str):
    """
    Запустить удаленное управление устройством
    
    Открывает окно scrcpy с экраном телефона
    """
    result = await device_manager.start_remote_control(device_id)
    return result

@router.post("/{device_id}/remote-control/stop")
async def stop_remote_control(device_id: str):
    """Закрыть окно удаленного управления"""
    result = await device_manager.stop_remote_control(device_id)
    return result

@router.get("/{device_id}/remote-control/status")
async def get_remote_control_status(device_id: str):
    """Проверить активен ли сеанс удаленного управления"""
    is_active = device_manager.remote_control.is_session_active(device_id)
    return {
        'device_id': device_id,
        'remote_control_active': is_active
    }
```

### 1.5 Frontend Component (frontend/src/components/RemoteControlButton.tsx)

```typescript
import React from 'react';
import { BiShow, BiHide } from 'react-icons/bi';
import { useApi } from '../hooks/useApi';
import { theme } from '../styles/theme';

interface RemoteControlButtonProps {
  deviceId: string;
  isActive: boolean;
}

export const RemoteControlButton: React.FC<RemoteControlButtonProps> = ({ 
  deviceId, 
  isActive 
}) => {
  const [loading, setLoading] = React.useState(false);
  const api = useApi();
  
  const handleRemoteControl = async () => {
    setLoading(true);
    try {
      if (isActive) {
        // Закрыть
        await api.post(`/devices/${deviceId}/remote-control/stop`);
      } else {
        // Открыть
        const response = await api.post(`/devices/${deviceId}/remote-control/start`);
        
        if (response.status === 'success') {
          // Показать уведомление
          window.dispatchEvent(new CustomEvent('show-notification', {
            detail: {
              type: 'success',
              message: response.message,
              duration: 3000
            }
          }));
        }
      }
    } catch (error) {
      window.dispatchEvent(new CustomEvent('show-notification', {
        detail: {
          type: 'error',
          message: 'Failed to control remote session'
        }
      }));
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <button
      onClick={handleRemoteControl}
      disabled={loading}
      style={{
        backgroundColor: isActive ? theme.colors.error : theme.colors.primary,
        color: 'white',
        border: 'none',
        padding: `${theme.spacing[2]} ${theme.spacing[4]}`,
        borderRadius: theme.borderRadius.base,
        cursor: loading ? 'not-allowed' : 'pointer',
        display: 'flex',
        alignItems: 'center',
        gap: theme.spacing[2],
        fontSize: theme.typography.fontSize.sm,
        fontWeight: theme.typography.fontWeight.medium,
        opacity: loading ? 0.7 : 1,
        transition: 'all 0.2s ease'
      }}
    >
      {isActive ? (
        <>
          <BiHide size={16} />
          Close Remote
        </>
      ) : (
        <>
          <BiShow size={16} />
          🔴 Live Control
        </>
      )}
    </button>
  );
};
```

### 1.6 Использование в DeviceCard (frontend/src/components/DeviceCard.tsx)

```typescript
import { RemoteControlButton } from './RemoteControlButton';

export const DeviceCard: React.FC<{ device: Device }> = ({ device }) => {
  const [remoteActive, setRemoteActive] = React.useState(false);
  
  React.useEffect(() => {
    // Проверить статус удаленного управления при загрузке
    checkRemoteStatus();
  }, []);
  
  const checkRemoteStatus = async () => {
    const response = await api.get(`/devices/${device.id}/remote-control/status`);
    setRemoteActive(response.remote_control_active);
  };
  
  return (
    <Card>
      {/* Другой контент карточки */}
      <DeviceInfo>
        <Status>{device.status}</Status>
        <Battery>{device.battery}%</Battery>
        <Temperature>{device.temperature}°C</Temperature>
      </DeviceInfo>
      
      {/* НОВОЕ: Кнопка удаленного управления */}
      <Actions>
        <RemoteControlButton 
          deviceId={device.id} 
          isActive={remoteActive}
        />
        <button>Restart</button>
        <button>Clear Cache</button>
      </Actions>
    </Card>
  );
};
```

---

## ЧАСТЬ 2: UIAUTOMATOR2 ИНТЕГРАЦИЯ (Programmatic UI Control)

### 2.1 Что это

**UIAutomator2** — это Python библиотека, которая:
- Подключается к Android устройству через ADB
- Получает иерархию UI элементов (XML)
- Кликает на элементы по селектору (ID, текст, класс и т.д.)
- Вводит текст, делает свайпы, прокрутки
- **НЕ требует GUI окна** — всё работает в фоне программно

**На телефоне:**
- ATX (Agent) — это фоновый агент, который слушает команды с ПК
- UIAutomator — Android фреймворк, через который ATX выполняет действия

### 2.2 Установка UIAutomator2

**На ПК:**
```bash
pip install uiautomator2
pip install pillow  # Для скриншотов
```

**На телефоне (автоматически через `init`):**
```bash
python -m uiautomator2 init --serial pixel-th-1:5555
```

Это установит ATX агент на телефон (увидишь иконку "UIAutomator" с меню опций).

### 2.3 Использование в Agents (backend/src/agents/)

**backend/src/agents/android_driver.py** (новый файл)

```python
import uiautomator2 as u2
from uiautomator2 import Device
import asyncio
import time
from typing import Optional, List, Tuple

class AndroidDriver:
    """
    Обертка вокруг uiautomator2
    Предоставляет удобный API для взаимодействия с UI
    """
    
    def __init__(self, serial: str, timeout: int = 10):
        """
        Инициализирует драйвер
        
        Args:
            serial: ADB serial (например, 'pixel-th-1:5555')
            timeout: таймаут для операций
        """
        self.serial = serial
        self.timeout = timeout
        self.d = None
    
    async def connect(self):
        """Подключиться к устройству"""
        try:
            self.d = u2.connect(self.serial)
            
            # Проверить живой ли ATX агент
            if not self.d.agent_alive:
                print(f"ATX agent not alive on {self.serial}, resetting...")
                self.d.reset_uiautomator()
                await asyncio.sleep(5)
            
            print(f"✅ Connected to {self.serial}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to {self.serial}: {e}")
            return False
    
    async def take_screenshot(self) -> bytes:
        """Получить скриншот"""
        return self.d.screenshot().tobytes()
    
    async def get_ui_hierarchy(self) -> str:
        """
        Получить иерархию UI (XML)
        Используется LLM для понимания UI структуры
        """
        return self.d.dump_hierarchy()
    
    async def click(self, x: int, y: int, duration: float = 0.1):
        """Клик по координатам"""
        self.d.click(x, y)
        await asyncio.sleep(duration)
    
    async def click_by_text(self, text: str, partial: bool = False):
        """Клик по тексту"""
        selector = self.d(text=text if not partial else f".*{text}.*", textContains=text if partial else None)
        if selector.exists:
            selector.click()
            await asyncio.sleep(0.2)
            return True
        return False
    
    async def click_by_resource_id(self, resource_id: str):
        """Клик по resource ID"""
        selector = self.d(resourceId=resource_id)
        if selector.exists:
            selector.click()
            await asyncio.sleep(0.2)
            return True
        return False
    
    async def type_text(self, text: str, clear_first: bool = True):
        """
        Ввести текст
        
        Args:
            text: текст для ввода
            clear_first: очистить поле перед вводом
        """
        if clear_first:
            self.d.send_keys(u'CTRL+a')
            await asyncio.sleep(0.1)
        
        # Вводим текст символ за символом (как human_typing)
        for char in text:
            self.d.send_keys(char)
            await asyncio.sleep(0.05)  # 50ms между символами
    
    async def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: float = 0.5):
        """Свайп"""
        self.d.swipe(x1, y1, x2, y2, duration)
        await asyncio.sleep(duration)
    
    async def scroll(self, direction: str = 'down', steps: int = 5):
        """
        Прокрутка
        
        Args:
            direction: 'up', 'down', 'left', 'right'
            steps: количество шагов
        """
        self.d.scroll(direction, steps)
        await asyncio.sleep(0.3)
    
    async def wait_for_element(self, text: str = None, resource_id: str = None, timeout: int = 5) -> bool:
        """Ждать появления элемента"""
        if text:
            return self.d(text=text).wait(timeout=timeout)
        elif resource_id:
            return self.d(resourceId=resource_id).wait(timeout=timeout)
        return False
    
    async def element_exists(self, text: str = None, resource_id: str = None) -> bool:
        """Проверить существует ли элемент"""
        if text:
            return self.d(text=text).exists
        elif resource_id:
            return self.d(resourceId=resource_id).exists
        return False
    
    async def get_element_text(self, resource_id: str) -> str:
        """Получить текст элемента"""
        return self.d(resourceId=resource_id).get_text()
    
    async def reset_uiautomator(self):
        """Перезагрузить ATX агент"""
        self.d.reset_uiautomator()
        await asyncio.sleep(5)
    
    async def close(self):
        """Закрыть соединение"""
        if self.d:
            self.d.close()

class UIAutomatorPool:
    """Пул драйверов для нескольких устройств"""
    
    def __init__(self):
        self.drivers = {}
    
    async def get_driver(self, serial: str) -> AndroidDriver:
        """Получить или создать драйвер"""
        if serial not in self.drivers:
            driver = AndroidDriver(serial)
            if await driver.connect():
                self.drivers[serial] = driver
            else:
                raise RuntimeError(f"Failed to connect to {serial}")
        
        return self.drivers[serial]
    
    async def close_all(self):
        """Закрыть все соединения"""
        for driver in self.drivers.values():
            await driver.close()
```

### 2.4 Использование в WhatsAppAgent

**backend/src/agents/whatsapp_agent.py** (обновленный)

```python
from .android_driver import AndroidDriver
import re

class WhatsAppAgent:
    """Отправляет WhatsApp сообщения"""
    
    def __init__(self, driver: AndroidDriver, llm_client, notion_client):
        self.driver = driver
        self.llm = llm_client
        self.notion = notion_client
    
    async def send_message(self, phone: str, text: str) -> bool:
        """
        Отправить одно сообщение
        
        Процесс:
        1. Открыть WhatsApp (если не открыт)
        2. Найти контакт по номеру
        3. Ввести сообщение
        4. Отправить
        5. Валидировать
        """
        
        try:
            # 1. Открыть WhatsApp
            await self.driver.click_by_resource_id('com.whatsapp:id/action_bar_search')
            await asyncio.sleep(0.5)
            
            # 2. Найти контакт (вводим номер телефона в поиск)
            await self.driver.type_text(phone)
            await asyncio.sleep(1)
            
            # 3. Кликнуть на контакт
            contact_found = await self.driver.click_by_text(phone)
            if not contact_found:
                return False
            
            await asyncio.sleep(1)
            
            # 4. Ввести сообщение в поле ввода
            await self.driver.click_by_resource_id('com.whatsapp:id/compose_area')
            await asyncio.sleep(0.3)
            await self.driver.type_text(text)
            await asyncio.sleep(0.5)
            
            # 5. Отправить
            await self.driver.click_by_resource_id('com.whatsapp:id/send')
            await asyncio.sleep(2)
            
            # 6. Валидировать (опционально, через скриншот и LLM)
            screenshot = await self.driver.take_screenshot()
            is_sent = await self.llm.analyze_screenshot(
                screenshot, 
                "Is the message successfully sent? Check for checkmarks or delivery indicators."
            )
            
            return "yes" in is_sent.lower()
        
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
```

---

## ЧАСТЬ 3: ИНТЕГРАЦИЯ AIRDROID (Резервный канал доступа)

### 3.1 Зачем

AirDroid — это web-интерфейс для управления Android через браузер. Если ADB/Scrcpy не работают (потеря коннекта), это резервный способ видеть экран телефона.

### 3.2 Установка на телефоне

1. Скачать AirDroid из Google Play
2. Авторизоваться
3. Записать URL вроде `https://my.airdroid.com/webstart/...`

### 3.3 Backend поддержка (backend/src/device_manager/manager.py)

```python
class Device:
    def __init__(self, device_id: str, adb_serial: str, airdroid_url: str = None):
        self.id = device_id
        self.adb_serial = adb_serial
        self.airdroid_url = airdroid_url  # Опционально
    
    async def get_access_urls(self) -> dict:
        """Получить все способы доступа к устройству"""
        return {
            'scrcpy': 'Built-in scrcpy',
            'airdroid': self.airdroid_url if self.airdroid_url else None,
            'adb': f'adb -s {self.adb_serial}'
        }
```

### 3.4 Frontend - кнопка для AirDroid (если нужна)

```typescript
<button onClick={() => window.open(device.airdroid_url, '_blank')}>
  📲 Open AirDroid Web
</button>
```

---

## ЧАСТЬ 4: ТРЕБОВАНИЯ K Requirements.txt

**backend/requirements.txt** (добавить/обновить):

```
# Существующие
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
httpx==0.25.1

# НОВЫЕ для Android автоматизации
uiautomator2==3.2.2        # UIAutomator2 Python wrapper
pillow==10.1.0             # Для скриншотов
adbutils==1.2.10           # ADB утилиты
python-dateutil==2.8.2

# Интеграции
notion-client==2.2.1
python-telegram-bot==20.3
google-generativeai==0.3.0

# Логирование
loguru==0.7.2

# Utils
tenacity==8.2.3
pyyaml==6.0.1
```

---

## ЧАСТЬ 5: ИНИЦИАЛИЗАЦИЯ픽셀'ЙОВ (Setup script)

**scripts/init_devices.py** (новый файл)

```python
#!/usr/bin/env python3
"""
Скрипт инициализации Android устройств
Должен быть запущен один раз перед первым использованием
"""

import subprocess
import sys

DEVICES = [
    {'id': 'pixel-th-1', 'serial': 'pixel-th-1:5555'},
    {'id': 'pixel-vn-1', 'serial': 'pixel-vn-1:5555'},
    {'id': 'pixel-th-2', 'serial': 'pixel-th-2:5555'},
]

def run_cmd(cmd):
    """Выполнить команду"""
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        return False
    print(f"✅ Success: {result.stdout}")
    return True

def init_device(device):
    """Инициализировать одно устройство"""
    print(f"\n{'='*60}")
    print(f"Initializing {device['id']} ({device['serial']})")
    print(f"{'='*60}")
    
    # 1. Проверить ADB видит устройство
    if not run_cmd(['adb', '-s', device['serial'], 'shell', 'echo', 'OK']):
        print(f"❌ Device {device['serial']} not found. Check ADB connection.")
        return False
    
    # 2. Инициализировать UIAutomator2
    print("\nInstalling UIAutomator2 agent...")
    if not run_cmd(['python', '-m', 'uiautomator2', 'init', '-s', device['serial']]):
        print(f"❌ Failed to install UIAutomator2")
        return False
    
    # 3. Проверить что ATX агент работает
    print("\nVerifying ATX agent...")
    try:
        import uiautomator2 as u2
        d = u2.connect(device['serial'])
        if d.agent_alive:
            print(f"✅ ATX agent is alive")
        else:
            print(f"⚠️  ATX agent not responding, resetting...")
            d.reset_uiautomator()
    except Exception as e:
        print(f"❌ Error checking ATX: {e}")
        return False
    
    print(f"\n✅ Device {device['id']} initialized successfully!\n")
    return True

def main():
    print("""
╔════════════════════════════════════════════════════════════════╗
║          Android Device Initialization Script                 ║
║                                                                ║
║  This will install UIAutomator2 agent on your devices         ║
║  Make sure all devices are connected via ADB before running   ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    input("Press Enter to continue...")
    
    success_count = 0
    for device in DEVICES:
        if init_device(device):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"Initialization complete: {success_count}/{len(DEVICES)} devices")
    print(f"{'='*60}\n")
    
    if success_count == len(DEVICES):
        print("✅ All devices ready! You can now run the application.")
        return 0
    else:
        print("❌ Some devices failed to initialize. Check errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

**Запуск:**
```bash
python scripts/init_devices.py
```

---

## ЧАСТЬ 6: ЧЕК-ЛИСТ ПЕРЕД ЗАПУСКОМ

### 6.1 Системные требования

- [ ] `scrcpy` установлен (`scrcpy --version`)
- [ ] `uiautomator2` установлен (`pip list | grep uiautomator2`)
- [ ] Все 3 Pixel'я подключены через ADB (`adb devices`)
- [ ] Tailscale настроен и работает
- [ ] Все Pixel'ы доступны через Tailscale IP

### 6.2 Инициализация устройств

- [ ] Запущен скрипт `python scripts/init_devices.py`
- [ ] На каждом Pixel'е видна иконка "UIAutomator" в меню
- [ ] Все три устройства вернули "OK" при инициализации

### 6.3 Scrcpy

- [ ] Есть мощность графики на ПК (scrcpy требует видео-кодирование)
- [ ] Bandwidth через VPN достаточно (рекомендуется 10+ Mbps)

### 6.4 Backend startup

При запуске backend (uvicorn) добавить логирование инициализации:

```python
@app.on_event("startup")
async def startup():
    # Инициализировать все устройства
    await device_manager.initialize()
    
    # Проверить что все подключены
    for device_id in ['pixel-th-1', 'pixel-vn-1', 'pixel-th-2']:
        status = await device_manager.get_device_status(device_id)
        if status['online']:
            print(f"✅ {device_id} online")
        else:
            print(f"❌ {device_id} offline - CHECK CONNECTION!")
```

---

## ИТОГО

Теперь у твоей системы есть:

✅ **Scrcpy** — видеть экран телефона и управлять мышкой  
✅ **UIAutomator2** — программно кликать, вводить текст, анализировать UI  
✅ **AirDroid** — резервный способ доступа через браузер  
✅ **Инициализационный скрипт** — автоматическая настройка всех устройств  

Это делает систему полностью готовой к реальной автоматизации WhatsApp, Instagram, LinkedIn и всего остального.
