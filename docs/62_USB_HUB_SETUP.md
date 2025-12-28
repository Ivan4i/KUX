# 62_USB_HUB_SETUP.md

## USB Hub Setup & Configuration

### Recommended Hardware

```
SETUP COMPONENTS:

1. USB Hub (7-port, USB 3.0 recommended)
   - Model: ANKER USB 3.0 Hub (7-port) or similar
   - Power: Individual port power or powered hub
   - Cost: $30-50
   - Specs: USB 3.0 (480 Mbps), 7 ports
   
2. USB Cables (High Quality)
   - Type: USB-A to USB-C (for modern Android)
   - Length: 1-2 meters (avoid too long)
   - Quality: Certified cables (Anker, Belkin)
   - Qty: 7 cables (one per device)
   
3. Developer Machine
   - OS: Linux (Ubuntu 20.04+) or Mac
   - CPU: 4+ cores (to handle 7 devices)
   - RAM: 8GB+ minimum (16GB recommended)
   - USB: USB 3.0 ports
   
4. Power Supply (Optional but Recommended)
   - Multi-port charger (7x USB-C or USB-A)
   - Keeps devices charged during operation
   - Prevents battery drain during testing
   
EXAMPLE SETUP (Cost ~$300-400):
┌──────────────────────────┐
│  Developer Machine       │  $1000+ (already have)
│  Linux/Mac with USB 3.0  │
└──────────────────────────┘
           ↓ USB Cable
┌──────────────────────────┐
│  USB 3.0 Hub (7-port)    │  $40
│  Anker/TP-Link model     │
└──────────────────────────┘
         ↙↙↙ 7x USB ↙↙↙
┌─────────────────────────────────┐
│ Android Phones (7x)              │  $200-350
│ - Used Samsung Galaxy S10-S20    │  (each ~$30-50 used)
│ - OR used Google Pixel 3-5       │
│ - Must support USB Debugging     │
└─────────────────────────────────┘
```

### USB Hub Installation

```bash
# Step 1: Identify USB Hub
lsusb  # List all USB devices

# Output example:
# Bus 003 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
# Bus 003 Device 002: ID 05e3:0612 Genesys Logic, Inc. Hub  ← This is your hub

# Step 2: Check USB 3.0 bandwidth
lsusb -t

# Output example (USB 3.0):
# /:  Bus 03.Port 1: Dev 1, Class=root_hub, Driver=xhci_hcd/6p, 480M

# If "480M" = USB 3.0 ✅
# If "12M" = USB 2.0 ❌ (too slow)

# Step 3: Verify all ports working
for port in {1..7}; do
    echo "Port $port: Testing..."
    # Plug device into port, watch dmesg
    dmesg | tail -1
done
```

### Device Connection Verification

```bash
# Step 1: Check ADB can see devices
adb devices -l

# Output:
# List of attached devices
# emulator-5554          device product:generic_x86 model:Android_SDK_built_for_x86
# RM0AA2A1AJJ            device product:t-mobile_us model:SM-G975U
# RM0AA2A1AKK            device product:t-mobile_us model:SM-G975U
# ...

# Step 2: Verify each device can execute commands
for device in $(adb devices | grep device | awk '{print $1}' | grep -v "List"); do
    echo "Testing $device..."
    adb -s $device shell getprop ro.product.model
    echo ""
done

# Step 3: Enable USB Debugging on each device
# (Manual: Settings > Developer Options > USB Debugging ON)

# Step 4: Authorize developer machine
# (Manual: On device, allow "RSA key" from computer)

# After first connection, accept authorization dialog on device
adb devices  # Should show "device" (not "unauthorized")
```

### Connection Stability Setup

```bash
#!/bin/bash
# setup_usb_connection.sh

echo "🔌 Setting up USB device connections..."

# Install necessary packages
sudo apt-get update
sudo apt-get install -y android-tools-adb android-tools-fastboot

# Verify ADB installed
adb version

# Add current user to android group (avoid sudo)
sudo usermod -a -G android $(whoami)
newgrp android

# Start ADB daemon
adb start-server

# Wait for devices
echo "Waiting for devices to appear..."
sleep 5

# List connected devices
echo "🎯 Connected devices:"
adb devices -l

# Test connection to each device
devices=$(adb devices | grep device | awk '{print $1}' | grep -v "List")
for device in $devices; do
    echo ""
    echo "Testing $device..."
    
    # Can we reach the device?
    if adb -s $device shell echo "OK" > /dev/null 2>&1; then
        echo "  ✅ $device: Connection OK"
    else
        echo "  ❌ $device: Connection FAILED"
    fi
done

echo ""
echo "✅ USB connection setup complete"
```

### Device-Specific Settings

```python
def prepare_device_for_testing(device_id: str, adb: ADBConnectionManager):
    """
    Configure device for automation testing.
    
    Disables features that might interfere with automation.
    """
    
    print(f"⚙️  Configuring {device_id}...")
    
    commands = [
        # Disable screen timeout
        ("shell settings put system screen_off_timeout 600000", "Screen timeout: 10 min"),
        
        # Disable animations (faster testing)
        ("shell settings put global window_animation_scale 0.0", "Window animations: OFF"),
        ("shell settings put global transition_animation_scale 0.0", "Transition animations: OFF"),
        ("shell settings put global animator_duration_scale 0.0", "Animator duration: OFF"),
        
        # Disable auto-rotation
        ("shell settings put system accelerometer_rotation 0", "Auto-rotate: OFF"),
        
        # Keep WiFi on during sleep
        ("shell settings put global wifi_sleep_policy 2", "WiFi sleep policy: NEVER"),
        
        # Disable battery saver
        ("shell settings put global low_power 0", "Battery saver: OFF"),
        
        # Disable lock screen
        ("shell locksettings set-disabled true", "Lock screen: DISABLED"),
        
        # Allow installation from unknown sources (if needed)
        ("shell settings put secure install_non_market_apps 1", "Unknown sources: ALLOWED"),
    ]
    
    for cmd, description in commands:
        try:
            result = subprocess.run(
                ["adb", "-s", device_id] + cmd.split(),
                capture_output=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print(f"  ✅ {description}")
            else:
                print(f"  ⚠️  {description} (failed)")
        
        except Exception as e:
            print(f"  ❌ {description}: {e}")

def configure_all_devices(device_ids: list):
    """Configure all devices in parallel."""
    
    from concurrent.futures import ThreadPoolExecutor
    
    adb = ADBConnectionManager()
    
    with ThreadPoolExecutor(max_workers=7) as executor:
        futures = [
            executor.submit(prepare_device_for_testing, device_id, adb)
            for device_id in device_ids
        ]
        
        for future in futures:
            future.result()
    
    print("✅ All devices configured")
```

### USB Hub Power Management

```bash
# Check power consumption per port
cat /sys/bus/usb/devices/*/power_level

# Optimize power settings for testing
# (Ensure devices don't sleep during testing)

# Check thermal status
echo "Checking device temperatures..."
for device in $(adb devices | grep device | awk '{print $1}' | grep -v "List"); do
    echo -n "$device: "
    adb -s $device shell cat /sys/class/thermal/thermal_zone0/temp | \
        awk '{print $1/1000 " °C"}'
done

# If overheating, reduce devices or add cooling
```

### Troubleshooting Connection Issues

```python
def diagnose_usb_connection(device_id: str) -> dict:
    """
    Diagnose USB connection issues.
    """
    
    diagnostics = {
        "device_id": device_id,
        "checks": {},
    }
    
    # Check 1: Is device in adb list?
    result = subprocess.run(
        ["adb", "devices"],
        capture_output=True,
        text=True
    )
    diagnostics["checks"]["adb_visible"] = device_id in result.stdout
    
    if not diagnostics["checks"]["adb_visible"]:
        print(f"❌ {device_id} not in adb devices list")
        print("   Solution: Check USB cable, try adb kill-server && adb start-server")
        return diagnostics
    
    # Check 2: Can we reach the device?
    result = subprocess.run(
        ["adb", "-s", device_id, "shell", "echo", "test"],
        capture_output=True,
        timeout=5
    )
    diagnostics["checks"]["shell_access"] = result.returncode == 0
    
    if not diagnostics["checks"]["shell_access"]:
        print(f"⚠️  {device_id} not responding to shell commands")
        print("   Solution: Device may be unauthorized. Check device display for auth prompt")
        return diagnostics
    
    # Check 3: Device properties
    result = subprocess.run(
        ["adb", "-s", device_id, "shell", "getprop", "ro.product.model"],
        capture_output=True,
        text=True
    )
    diagnostics["model"] = result.stdout.strip()
    
    # Check 4: Battery level
    result = subprocess.run(
        ["adb", "-s", device_id, "shell", "dumpsys", "battery"],
        capture_output=True,
        text=True
    )
    
    for line in result.stdout.split("\n"):
        if "level:" in line:
            diagnostics["battery"] = line.split()[-1] + "%"
    
    # All checks passed
    diagnostics["status"] = "OK" if all(diagnostics["checks"].values()) else "ISSUES"
    
    return diagnostics

# Run diagnostics on all devices
def run_full_diagnostics():
    devices = subprocess.run(
        ["adb", "devices"],
        capture_output=True,
        text=True
    ).stdout
    
    device_ids = [
        line.split()[0]
        for line in devices.split("\n")[1:]
        if "\t" in line and "device" in line
    ]
    
    print("\n📊 USB Connection Diagnostics:")
    print("─" * 50)
    
    for device_id in device_ids:
        diag = diagnose_usb_connection(device_id)
        print(f"{device_id}:")
        print(f"  Status: {diag['status']}")
        print(f"  Model: {diag.get('model', 'Unknown')}")
        print(f"  Battery: {diag.get('battery', 'Unknown')}")
```

---

## End of 62_USB_HUB_SETUP.md