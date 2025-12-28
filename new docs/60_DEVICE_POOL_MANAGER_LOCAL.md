# 60_DEVICE_POOL_MANAGER_LOCAL.md

## Local Device Pool Management (USB-Based)

### Architecture: Simplified Local Setup

```
┌─────────────────────────────────────────┐
│     Developer Machine (Linux/Mac)       │
│                                         │
│  ┌──────────────────────────────────┐   │
│  │   Device Pool Manager (Python)   │   │
│  │   - Monitors all USB devices     │   │
│  │   - Tracks device state          │   │
│  │   - Distributes tasks            │   │
│  └──────────────────────────────────┘   │
│                                         │
│  ┌─────────────┬──────────┬──────────┐  │
│  │   ADB       │ scrcpy   │ File I/O │  │
│  │ (commands)  │ (screen) │ (storage)│  │
│  └─────────────┴──────────┴──────────┘  │
└─────────────────────────────────────────┘
           ↓↓↓ USB 3.0 ↓↓↓
┌──────────────────────────────────────────────┐
│         USB Hub (7-port)                     │
├──────────────────────────────────────────────┤
│ [Device1] [Device2] [Device3] [Device4]     │
│ [Device5] [Device6] [Device7]               │
└──────────────────────────────────────────────┘

All communication: Local USB only (no network needed)
Performance: Direct USB 3.0 (480Mbps)
Latency: <50ms per command
Reliability: 99.9% (USB is stable)
```

### DevicePoolManager Class

```python
class DevicePoolManager:
    """
    Manage physical Android devices connected via USB.
    
    Responsibilities:
    - Track device connections/disconnections
    - Maintain device state (battery, temperature, storage)
    - Distribute tasks to available devices
    - Handle device failures and recovery
    - Implement device rotation (load balancing)
    """
    
    def __init__(self, max_devices: int = 7):
        self.max_devices = max_devices
        self.devices: dict[str, DeviceInfo] = {}
        self.task_queue: list = []
        self.monitoring_enabled = False
    
    def initialize(self):
        """Initialize device manager."""
        print("🔌 Initializing Device Pool Manager...")
        
        # Step 1: Check ADB
        if not self.check_adb_installed():
            raise RuntimeError("❌ ADB not installed. Install Android SDK.")
        
        # Step 2: Detect connected devices
        self.refresh_device_list()
        
        # Step 3: Start monitoring
        self.start_monitoring()
        
        print(f"✅ Device Pool Ready: {len(self.devices)} devices detected")
    
    def check_adb_installed(self) -> bool:
        """Verify ADB is installed and accessible."""
        try:
            result = subprocess.run(
                ["adb", "version"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def refresh_device_list(self):
        """Scan for all connected USB devices."""
        print("📱 Scanning for connected devices...")
        
        try:
            result = subprocess.run(
                ["adb", "devices", "-l"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            lines = result.stdout.strip().split("\n")[1:]  # Skip header
            
            for line in lines:
                if not line.strip():
                    continue
                
                parts = line.split()
                device_id = parts[0]
                status = parts[1]
                
                if status == "device":
                    if device_id not in self.devices:
                        self.devices[device_id] = DeviceInfo(
                            device_id=device_id,
                            connection_type="usb",
                        )
                        print(f"  ✅ Found: {device_id}")
                    
                    # Update device info
                    self.devices[device_id].update_state()
        
        except Exception as e:
            print(f"❌ Error scanning devices: {e}")
    
    def start_monitoring(self):
        """Start continuous monitoring of devices."""
        self.monitoring_enabled = True
        
        # Start background monitor thread
        monitor_thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True
        )
        monitor_thread.start()
        print("👁️  Device monitoring started")
    
    def _monitor_loop(self):
        """Continuous monitoring (runs in background)."""
        while self.monitoring_enabled:
            try:
                # Check device connections
                self.refresh_device_list()
                
                # Check device health
                for device_id, device_info in self.devices.items():
                    device_info.check_health()
                
                # Log status every 30 seconds
                time.sleep(30)
                self._log_pool_status()
            
            except Exception as e:
                print(f"⚠️  Monitoring error: {e}")
                time.sleep(5)
    
    def get_available_device(self) -> "DeviceInfo":
        """
        Get the best available device for task.
        
        Priority:
        1. Device with lowest load
        2. Device with highest battery
        3. Device with lowest temperature
        """
        
        available = [
            d for d in self.devices.values()
            if d.status == "healthy" and not d.is_busy
        ]
        
        if not available:
            raise RuntimeError("❌ No available devices")
        
        # Sort by load (ascending)
        available.sort(key=lambda d: d.current_load)
        
        return available[0]
    
    def assign_task(self, task: dict) -> str:
        """
        Assign task to best available device.
        
        Returns: device_id
        """
        device = self.get_available_device()
        
        device.assign_task(task)
        print(f"📋 Task assigned to {device.device_id}: {task['name']}")
        
        return device.device_id
    
    def _log_pool_status(self):
        """Log status of entire device pool."""
        print("\n📊 DEVICE POOL STATUS:")
        print(f"{'Device':<15} {'Battery':<12} {'Temp':<12} {'Load':<10} {'Status':<10}")
        print("─" * 60)
        
        for device_id, device_info in self.devices.items():
            battery = f"{device_info.battery_level}%"
            temp = f"{device_info.temperature}°C"
            load = f"{device_info.current_load}%"
            status = device_info.status
            
            print(f"{device_id:<15} {battery:<12} {temp:<12} {load:<10} {status:<10}")
```

### DeviceInfo Class

```python
class DeviceInfo:
    """Information and state for a single device."""
    
    def __init__(self, device_id: str, connection_type: str = "usb"):
        self.device_id = device_id
        self.connection_type = connection_type
        self.status = "initializing"  # initializing, healthy, warning, error
        self.battery_level = 0
        self.temperature = 0
        self.storage_used = 0
        self.current_load = 0  # Percentage of capacity used
        self.is_busy = False
        self.current_task = None
        self.last_heartbeat = time.time()
    
    def update_state(self):
        """Update device state from ADB."""
        try:
            # Battery level
            result = subprocess.run(
                ["adb", "-s", self.device_id, "shell", "dumpsys", "battery"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            for line in result.stdout.split("\n"):
                if "level:" in line:
                    self.battery_level = int(line.split()[-1])
            
            # Temperature
            result = subprocess.run(
                ["adb", "-s", self.device_id, "shell", "cat", "/sys/class/thermal/thermal_zone0/temp"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.stdout:
                # Convert from millidegrees to degrees
                self.temperature = int(result.stdout.strip()) / 1000
            
            self.last_heartbeat = time.time()
            self.check_health()
        
        except Exception as e:
            print(f"⚠️  Error updating {self.device_id}: {e}")
            self.status = "error"
    
    def check_health(self):
        """Check device health status."""
        # Check battery
        if self.battery_level < 10:
            self.status = "warning"
            return
        
        # Check temperature
        if self.temperature > 45:
            self.status = "warning"
            return
        
        # Check heartbeat (is device responding?)
        if time.time() - self.last_heartbeat > 60:
            self.status = "error"
            return
        
        # All good
        self.status = "healthy"
    
    def assign_task(self, task: dict):
        """Assign task to this device."""
        self.is_busy = True
        self.current_task = task
        self.current_load = min(100, self.current_load + 25)
    
    def complete_task(self):
        """Mark task as complete."""
        self.is_busy = False
        self.current_task = None
        self.current_load = max(0, self.current_load - 25)
```

### Device Connection Management

```python
def connect_all_devices():
    """Ensure all devices connected and authorized."""
    
    print("🔗 Connecting to all devices...")
    
    # Get list of devices
    result = subprocess.run(
        ["adb", "devices"],
        capture_output=True,
        text=True
    )
    
    devices = []
    for line in result.stdout.split("\n")[1:]:
        if "\t" in line:
            device_id = line.split("\t")[0]
            devices.append(device_id)
    
    # Connect and authorize each
    for device_id in devices:
        try:
            # Get device info
            subprocess.run(
                ["adb", "-s", device_id, "shell", "echo", "test"],
                capture_output=True,
                timeout=5
            )
            print(f"  ✅ {device_id}: Connected & Authorized")
        
        except Exception as e:
            print(f"  ⚠️  {device_id}: {e}")

def disconnect_all_devices():
    """Safely disconnect all devices."""
    
    print("🔌 Disconnecting all devices...")
    
    result = subprocess.run(
        ["adb", "devices"],
        capture_output=True,
        text=True
    )
    
    for line in result.stdout.split("\n")[1:]:
        if "\t" in line:
            device_id = line.split("\t")[0]
            subprocess.run(["adb", "-s", device_id, "shell", "exit"])
    
    print("✅ All devices disconnected")
```

---

## Usage Example

```python
# Initialize pool
pool = DevicePoolManager(max_devices=7)
pool.initialize()

# Get available device
device = pool.get_available_device()
print(f"📱 Using device: {device.device_id}")

# Assign tasks
for task in task_list:
    device_id = pool.assign_task(task)
    # Execute task...
    device_info = pool.devices[device_id]
    device_info.complete_task()

# Status
pool._log_pool_status()
```

---

## End of 60_DEVICE_POOL_MANAGER_LOCAL.md