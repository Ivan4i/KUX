# 61_USB_ADB_PERSISTENT_CONNECTION.md

## USB ADB Persistent Connections

### ADB Over USB: Direct Connection

```
Device Configuration:
┌──────────────────────────────┐
│     Android Device (USB)     │
├──────────────────────────────┤
│ Settings > Developer Options │
│ ✅ USB Debugging: ON         │
│ ✅ MTP Mode (or ADB mode)    │
│ ✅ File Transfer Enabled     │
└──────────────────────────────┘
           ↓ USB Cable
┌──────────────────────────────┐
│  Developer Machine (ADB)     │
│  adb devices -l              │
│  adb connect <device_serial> │
└──────────────────────────────┘

USB Properties:
- Direct connection (no network)
- 480 Mbps (USB 3.0: up to 5 Gbps)
- Latency: ~20-50ms per command
- Reliability: Stable (wired connection)
- Power: Device charges while connected
```

### ADB Connection Manager

```python
class ADBConnectionManager:
    """
    Manage persistent ADB connections over USB.
    
    Key features:
    - Auto-detect devices
    - Handle disconnections
    - Keep connections alive (heartbeat)
    - Parallel command execution
    """
    
    def __init__(self):
        self.connections = {}  # device_id -> connection_obj
        self.heartbeat_interval = 60  # seconds
        self.command_timeout = 30  # seconds
    
    def detect_devices(self) -> list:
        """Detect all USB-connected devices."""
        
        try:
            result = subprocess.run(
                ["adb", "devices", "-l"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            devices = []
            for line in result.stdout.split("\n")[1:]:
                if "\t" not in line or "device" not in line:
                    continue
                
                device_id = line.split("\t")[0]
                devices.append(device_id)
                
                print(f"  📱 Found: {device_id}")
            
            return devices
        
        except Exception as e:
            print(f"❌ Error detecting devices: {e}")
            return []
    
    def connect_device(self, device_id: str) -> bool:
        """
        Establish persistent connection to device.
        
        USB devices typically connect automatically.
        No IP:port needed for USB (unlike TCP/IP).
        """
        
        print(f"🔗 Connecting to {device_id}...")
        
        try:
            # Check if device is already in adb devices list
            result = subprocess.run(
                ["adb", "devices"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if device_id in result.stdout:
                # Device is already connected
                self.connections[device_id] = {
                    "status": "connected",
                    "device_id": device_id,
                    "last_heartbeat": time.time(),
                    "connection_type": "usb",
                }
                
                print(f"  ✅ {device_id}: Connected")
                return True
            else:
                print(f"  ❌ {device_id}: Not found")
                return False
        
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return False
    
    def disconnect_device(self, device_id: str):
        """Disconnect device safely."""
        
        try:
            subprocess.run(
                ["adb", "-s", device_id, "disconnect"],
                capture_output=True,
                timeout=5
            )
            
            if device_id in self.connections:
                del self.connections[device_id]
            
            print(f"  ✅ {device_id}: Disconnected")
        
        except Exception as e:
            print(f"  ❌ Error disconnecting: {e}")
    
    def execute_command(self, device_id: str, command: str) -> str:
        """
        Execute ADB command on device.
        
        Example:
            result = adb.execute_command(
                "emulator-5554",
                "shell input text 'hello world'"
            )
        """
        
        if device_id not in self.connections:
            raise RuntimeError(f"Device {device_id} not connected")
        
        try:
            full_command = ["adb", "-s", device_id] + command.split()
            
            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                timeout=self.command_timeout
            )
            
            # Update heartbeat
            self.connections[device_id]["last_heartbeat"] = time.time()
            
            return result.stdout.strip()
        
        except subprocess.TimeoutExpired:
            print(f"⏱️  Command timeout on {device_id}")
            return None
        
        except Exception as e:
            print(f"❌ Error executing command: {e}")
            return None
    
    def push_file(self, device_id: str, local_path: str, remote_path: str) -> bool:
        """Push file to device."""
        
        try:
            result = subprocess.run(
                ["adb", "-s", device_id, "push", local_path, remote_path],
                capture_output=True,
                timeout=60
            )
            
            self.connections[device_id]["last_heartbeat"] = time.time()
            
            return result.returncode == 0
        
        except Exception as e:
            print(f"❌ Error pushing file: {e}")
            return False
    
    def pull_file(self, device_id: str, remote_path: str, local_path: str) -> bool:
        """Pull file from device."""
        
        try:
            result = subprocess.run(
                ["adb", "-s", device_id, "pull", remote_path, local_path],
                capture_output=True,
                timeout=60
            )
            
            self.connections[device_id]["last_heartbeat"] = time.time()
            
            return result.returncode == 0
        
        except Exception as e:
            print(f"❌ Error pulling file: {e}")
            return False
    
    def start_heartbeat_monitor(self):
        """Monitor connection health (background thread)."""
        
        def monitor():
            while True:
                try:
                    for device_id, conn in list(self.connections.items()):
                        elapsed = time.time() - conn["last_heartbeat"]
                        
                        if elapsed > self.heartbeat_interval * 2:
                            # Connection seems dead, try to reconnect
                            print(f"⚠️  {device_id}: No heartbeat, reconnecting...")
                            self.connect_device(device_id)
                    
                    time.sleep(self.heartbeat_interval)
                
                except Exception as e:
                    print(f"❌ Heartbeat monitor error: {e}")
                    time.sleep(5)
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
        print("👁️  Heartbeat monitor started")
```

### ADB Commands for Common Tasks

```python
def get_adb_commands(device_id: str) -> dict:
    """
    Dictionary of common ADB commands for device control.
    """
    
    def adb_cmd(cmd):
        return f"adb -s {device_id} {cmd}"
    
    return {
        # Screen Control
        "turn_on_screen": adb_cmd("shell input keyevent 26"),
        "turn_off_screen": adb_cmd("shell input keyevent 26"),
        "unlock": adb_cmd("shell input keyevent 82"),
        "lock": adb_cmd("shell input keyevent 26 26"),
        
        # Navigation
        "press_home": adb_cmd("shell input keyevent 3"),
        "press_back": adb_cmd("shell input keyevent 4"),
        "press_recent": adb_cmd("shell input keyevent 187"),
        
        # Text Input
        "type_text": adb_cmd("shell input text '{text}'"),  # Placeholder
        "press_enter": adb_cmd("shell input keyevent 66"),
        "press_delete": adb_cmd("shell input keyevent 67"),
        
        # App Control
        "open_app": adb_cmd("shell am start -n {package}/{activity}"),
        "close_app": adb_cmd("shell am force-stop {package}"),
        
        # Device Info
        "get_battery": adb_cmd("shell dumpsys battery"),
        "get_device_name": adb_cmd("shell getprop ro.product.model"),
        "get_android_version": adb_cmd("shell getprop ro.build.version.release"),
        "get_storage": adb_cmd("shell df /data"),
    }

def execute_adb_command(device_id: str, command: str, **kwargs) -> bool:
    """Execute ADB command with placeholder substitution."""
    
    # Replace placeholders
    for key, value in kwargs.items():
        command = command.replace(f"{{{key}}}", value)
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            timeout=30
        )
        
        return result.returncode == 0
    
    except Exception as e:
        print(f"❌ Command failed: {e}")
        return False
```

### Connection Pooling

```python
class ADBConnectionPool:
    """
    Pool of persistent ADB connections for efficiency.
    
    Benefits:
    - Reuse connections (faster)
    - Avoid connection overhead
    - Better error recovery
    """
    
    def __init__(self, max_connections: int = 7):
        self.max_connections = max_connections
        self.connections = {}
        self.manager = ADBConnectionManager()
    
    def initialize(self):
        """Initialize connection pool."""
        
        print("🔌 Initializing ADB Connection Pool...")
        
        # Detect devices
        devices = self.manager.detect_devices()
        
        # Connect to all
        for device_id in devices[:self.max_connections]:
            if self.manager.connect_device(device_id):
                self.connections[device_id] = self.manager.connections[device_id]
        
        print(f"✅ Connected to {len(self.connections)} devices")
    
    def get_connection(self, device_id: str):
        """Get connection from pool."""
        
        if device_id not in self.connections:
            raise RuntimeError(f"Connection {device_id} not in pool")
        
        return self.connections[device_id]
    
    def execute_on_device(self, device_id: str, cmd: str) -> str:
        """Execute command on device from pool."""
        
        conn = self.get_connection(device_id)
        return self.manager.execute_command(device_id, cmd)
    
    def close_all(self):
        """Close all connections."""
        
        for device_id in list(self.connections.keys()):
            self.manager.disconnect_device(device_id)
        
        print("✅ All connections closed")
```

---

## End of 61_USB_ADB_PERSISTENT_CONNECTION.md