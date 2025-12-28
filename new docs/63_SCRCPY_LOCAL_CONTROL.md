# 63_SCRCPY_LOCAL_CONTROL.md

## scrcpy: Local Screen Mirroring & Control

### What is scrcpy?

```
scrcpy = Stream Copy (from device to computer)

Purpose:
- Mirror Android screen to computer display
- Control device from keyboard/mouse
- Record session video
- Capture screenshots
- All over USB (no WiFi needed!)

Benefits:
✅ See exactly what's happening on device
✅ Manual intervention when needed
✅ Debug automation issues
✅ Monitor multiple devices simultaneously
✅ Local USB connection (fast, reliable)

Performance:
- Latency: 20-50ms (USB)
- Resolution: Up to device native (1080p+)
- Frame rate: 30-60 fps
- CPU Usage: Low (hardware acceleration)
```

### Installation

```bash
# Linux (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y scrcpy

# Verify installation
scrcpy --version

# macOS (using Homebrew)
brew install scrcpy

# Windows (using chocolatey)
choco install scrcpy

# Or build from source
git clone https://github.com/Genymobile/scrcpy.git
cd scrcpy
meson setup build
ninja -C build
sudo ninja -C build install
```

### Basic Usage

```bash
# Mirror single device to screen
scrcpy -s <device_id>

# Mirror with specific resolution (faster)
scrcpy -s <device_id> -m 720  # Scale to 720p

# Mirror with custom frame rate
scrcpy -s <device_id> -f 30   # 30 fps (vs default 60)

# Record to file
scrcpy -s <device_id> --record=video.mp4

# No video (audio only)
scrcpy -s <device_id> --no-video

# Show touch points (debug)
scrcpy -s <device_id> --show-touches

# Record and display simultaneously
scrcpy -s <device_id> --record=session.mp4 --render-expired-frames
```

### Keyboard & Mouse Control

```bash
# Control device from keyboard (when scrcpy window is focused):

# Text input
type text normally → sends to device

# Special keys
Ctrl+Home       → Power button
Ctrl+End        → App switcher
Ctrl+F          → Turn on/off screen
Ctrl+U          → Screenshot
Ctrl+V          → Paste from clipboard
Ctrl+N          → Expand notifications
Ctrl+B          → Go back
Ctrl+Home       → Go home
Ctrl+S          → Open app drawer

# Mouse control
Left click      → Tap at cursor position
Right click     → Back button
Scroll wheel    → Scroll in app
```

### Multi-Device Mirroring

```bash
#!/bin/bash
# monitor_all_devices.sh
# Mirror all connected devices to separate windows

echo "Starting scrcpy for all devices..."

# Get all connected devices
devices=$(adb devices | grep device | awk '{print $1}' | grep -v "List")

# Start scrcpy for each device (each in new window)
for device in $devices; do
    echo "Starting scrcpy for $device..."
    
    # Open in new terminal window (Linux/Mac)
    gnome-terminal -- scrcpy -s $device -m 720 --always-on-top &
    
    # macOS alternative:
    # open -a Terminal <<"EOF"
    # scrcpy -s $device -m 720 --always-on-top
    # EOF
    
    sleep 1
done

echo "✅ All devices mirrored. Press Ctrl+C to stop."
```

### scrcpy Control Library (Python)

```python
import subprocess
import time
import threading

class ScrcpyController:
    """
    Control scrcpy instances programmatically.
    
    Useful for:
    - Automated UI verification
    - Visual debugging
    - Recording test sessions
    """
    
    def __init__(self, device_id: str, resolution: int = 720):
        self.device_id = device_id
        self.resolution = resolution
        self.process = None
        self.recording_file = None
    
    def start_mirror(self, record_video: bool = False):
        """Start scrcpy screen mirroring."""
        
        print(f"🎥 Starting scrcpy for {self.device_id}...")
        
        cmd = [
            "scrcpy",
            "-s", self.device_id,
            "-m", str(self.resolution),
            "--always-on-top",
            "--no-audio",  # Reduces CPU usage
        ]
        
        if record_video:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            self.recording_file = f"recording_{self.device_id}_{timestamp}.mp4"
            cmd.extend(["--record", self.recording_file])
            print(f"  📹 Recording to: {self.recording_file}")
        
        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"  ✅ scrcpy started (PID: {self.process.pid})")
        
        except Exception as e:
            print(f"  ❌ Failed to start scrcpy: {e}")
    
    def stop_mirror(self):
        """Stop scrcpy."""
        
        if self.process:
            self.process.terminate()
            self.process.wait()
            print(f"✅ scrcpy stopped")
            
            if self.recording_file:
                print(f"✅ Recording saved: {self.recording_file}")
    
    def take_screenshot(self, output_file: str = None) -> str:
        """Take screenshot of device screen."""
        
        if not output_file:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = f"screenshot_{self.device_id}_{timestamp}.png"
        
        cmd = ["adb", "-s", self.device_id, "shell", "screencap", "-p"]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=10
            )
            
            # Save to file
            with open(output_file, "wb") as f:
                f.write(result.stdout)
            
            print(f"📸 Screenshot saved: {output_file}")
            return output_file
        
        except Exception as e:
            print(f"❌ Screenshot failed: {e}")
            return None

class MultiDeviceMonitor:
    """
    Monitor multiple devices simultaneously.
    
    Example:
        monitor = MultiDeviceMonitor(["device1", "device2"])
        monitor.start_all()
        # View all devices in separate windows
    """
    
    def __init__(self, device_ids: list, resolution: int = 720):
        self.device_ids = device_ids
        self.resolution = resolution
        self.controllers = {}
    
    def start_all(self, record: bool = False):
        """Start mirroring all devices."""
        
        print(f"🎥 Starting {len(self.device_ids)} devices...")
        
        for device_id in self.device_ids:
            controller = ScrcpyController(device_id, self.resolution)
            
            # Start each in separate thread
            thread = threading.Thread(
                target=controller.start_mirror,
                args=(record,),
                daemon=True
            )
            thread.start()
            
            self.controllers[device_id] = controller
            time.sleep(2)  # Stagger starts
        
        print(f"✅ All {len(self.device_ids)} devices mirroring")
    
    def stop_all(self):
        """Stop all devices."""
        
        for device_id, controller in self.controllers.items():
            controller.stop_mirror()
        
        print(f"✅ All devices stopped")

# Usage example
if __name__ == "__main__":
    # Single device
    controller = ScrcpyController("device1", resolution=720)
    controller.start_mirror(record_video=True)
    
    # Let it run for 30 seconds
    time.sleep(30)
    
    # Take screenshot
    controller.take_screenshot()
    
    # Stop
    controller.stop_mirror()
    
    # Multiple devices
    print("\n---\n")
    
    monitor = MultiDeviceMonitor(["device1", "device2", "device3"])
    monitor.start_all(record=True)
    
    # Run for 2 minutes
    time.sleep(120)
    
    # Stop all
    monitor.stop_all()
```

### Debugging with scrcpy

```python
def debug_automation_with_scrcpy(device_id: str, test_function, record: bool = True):
    """
    Run automation while recording screen (for debugging).
    
    Useful for:
    - Identifying where automation fails
    - Verifying correct behavior
    - Creating demos/documentation
    """
    
    # Start recording
    controller = ScrcpyController(device_id, resolution=720)
    controller.start_mirror(record_video=record)
    
    # Wait for UI to load
    time.sleep(2)
    
    try:
        # Run the test/automation
        print("🤖 Running automation...")
        result = test_function(device_id)
        
        print(f"✅ Automation completed: {result}")
    
    except Exception as e:
        print(f"❌ Automation failed: {e}")
    
    finally:
        # Always stop recording
        time.sleep(1)
        controller.stop_mirror()
```

### Advanced: Custom Commands

```bash
# Full command with all options
scrcpy \
    -s <device_id> \
    -m 720 \                    # Resolution
    -f 30 \                     # Frame rate
    --always-on-top \           # Window stays on top
    --no-audio \                # No audio (faster)
    --record=output.mp4 \       # Record video
    --show-touches \            # Show finger positions
    --render-expired-frames     # Better visuals

# Monitor with keyboard shortcuts displayed
scrcpy -s <device_id> --show-touches --print-fps

# Minimal mirror (smallest window, fastest)
scrcpy -s <device_id> -m 480 -f 15 --no-audio

# Large mirror (for presentation)
scrcpy -s <device_id> -m 1080 -f 60
```

### Integration with Automation

```python
def run_automation_with_monitoring(
    device_id: str,
    automation_steps: list,
    monitor: bool = True,
    record: bool = True,
):
    """
    Run automation with optional screen monitoring.
    
    If monitoring enabled:
    - Show screen in real-time
    - Save recording
    - Better debugging
    """
    
    controller = ScrcpyController(device_id) if monitor else None
    
    if controller:
        controller.start_mirror(record_video=record)
        time.sleep(2)
    
    try:
        for step in automation_steps:
            print(f"Executing: {step['name']}")
            
            # Execute automation step
            if step["type"] == "click":
                adb.click(device_id, step["x"], step["y"])
            elif step["type"] == "type":
                adb.type_text(device_id, step["text"])
            elif step["type"] == "wait":
                time.sleep(step["duration"])
            
            # Screenshot after important steps
            if step.get("screenshot"):
                controller.take_screenshot(f"step_{step['name']}.png")
            
            time.sleep(step.get("delay", 0.5))
    
    finally:
        if controller:
            controller.stop_mirror()
```

---

## End of 63_SCRCPY_LOCAL_CONTROL.md