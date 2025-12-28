# 📱 DEVICE TOPOLOGY: 20 Devices + USB Hub (LOCAL ONLY)

## Physical Layout

### USB Hub Configuration

**ORICO USB 3.0 Hub (10 ports)**

```
            ┌─────────────────────────────┐
            │    ORICO USB 3.0 Hub        │
            │     (10 ports, daisy)       │
            └─────────────────────────────┘
                    │ (Daisy-chain cable to 2nd hub)
                    │
     ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
     │Port1 │Port2 │Port3 │Port4 │Port5 │Port6 │Port7 │Port8 │Port9 │Port10│
     └──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘
       │      │      │      │      │      │      │      │      │      │
     Dev1   Dev2   Dev3   Dev4   Dev5   Dev6   Dev7   Dev8   Dev9  Dev10
     │      │      │      │      │      │      │      │      │      │
   Pixel5  Pixel5 Pixel5 Pixel5 Pixel5 Pixel5 Pixel5 Pixel5 Pixel5 Pixel5
  #001    #002   #003   #004   #005   #006   #007   #008   #009   #010

    (Similarly, Port 2nd Hub: Device #011-#020)
```

### Hub Specifications

```
Model: ORICO USB 3.0 Hub
Ports: 10 (per hub) × 2 hubs = 20 total
Power: External 12V/2A (for each hub)
Cable: USB 3.0 Type-A upstream to Mac
Speed: 5 Gbps per port
Maximum devices: 20 (meets requirement exactly)
Daisy-chain: Two hubs connected via daisy-cable
Price: ~$30 per hub (affordable, replaceable)
```

---

## Device Inventory (20 × Google Pixel 5)

### Device Specifications

```
Model: Google Pixel 5
Processor: Snapdragon 765G
RAM: 8GB
Storage: 128GB
Screen: 6.0" (1080p)
Battery: 4080 mAh (full-day usage)
Android: 14 (upgradeable)
Network: WiFi 6E, Bluetooth 5.2

Key for automation:
✅ USB Debugging: Enabled (always on)
✅ Developer Mode: Enabled
✅ ADB Wireless Mode: Enabled (TCP 5555)
✅ UIAutomator2: Available (system app)
✅ Screenshot: Via ADB (600-800 KB per shot)
✅ SIM Card: Corporate SMS plan (1000/day limit)
```

### Device Naming Convention

```
device-01 through device-20

Physical stickers on devices:
  • Barcode label: DEV-001, DEV-002, etc
  • Location tag: HUB1-P01, HUB1-P02, ... HUB2-P01, etc
  • Phone number: Printed on charger
  
Database mapping:
  device-01 → ADB serial "R3CR5000A001"
  device-02 → ADB serial "R3CR5000A002"
  ...
  device-20 → ADB serial "R3CR5000A020"
```

---

## ADB Connection Topology

### USB Mode (Primary - Always Connected)

```
┌──────────────────────────────────────────────┐
│            Mac (Orchestrator)                │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │     Backend Service (FastAPI)          │ │
│  │   • ADB shell commands                 │ │
│  │   • Device monitoring (every 30 sec)   │ │
│  │   • Task allocation (round-robin)      │ │
│  └────────────────────────────────────────┘ │
│              │ (ADB over USB)               │
│              ↓                               │
│  ┌────────────────────────────────────────┐ │
│  │    ADB Daemon (localhost:5037)         │ │
│  │    (bridges to USB devices)            │ │
│  └────────────────────────────────────────┘ │
└──────────────────────────────────────────────┘
      │ (USB 3.0 cables - 20 cables)
      │
      ├─ Device 1 (ADB daemon on device)
      ├─ Device 2
      ├─ ...
      └─ Device 20

Connection speed: USB 3.0 = 5 Gbps per device
Actual throughput: 50-100 Mbps (plenty for ADB)
Latency: < 5 ms per command (local USB)
```

### TCP Mode (Fallback - Wireless)

```
If USB connection fails:
  • Switch to WiFi TCP mode (192.168.x.x:5555)
  • Requires: adb connect {device_ip}:5555
  • Used only as fallback (slower, less reliable)
  • Automatic failover: USB → TCP → USB (retry)
```

---

## Device Network Configuration

### WiFi Setup (Optional, for TCP Fallback)

```
Each device:
  • Connected to same WiFi as Mac
  • DHCP enabled (auto IP assignment)
  • WiFi password saved in device settings
  
Network range: 192.168.1.0/24 (typical home network)
Device IPs: 192.168.1.100 - 192.168.1.119 (allocated)
Gateway: 192.168.1.1 (router)
DNS: Auto (from router)

Fallback scenario:
  If USB unplugs → auto-switch to TCP
  Command: adb connect 192.168.1.100:5555
  Latency: 50-200 ms (higher than USB)
  Timeout: 10 sec (vs 5 sec for USB)
```

---

## Device Partitioning & Load Balancing

### Physical Arrangement (For Cooling & Accessibility)

```
Setup 1: Horizontal Rack (Desktop)

USB Hub 1 (10 devices):
  ┌─ Device 1  ┌─ Device 2  ┌─ Device 3  ┌─ Device 4  ┌─ Device 5
  │ (hub 1-p1)  │ (hub 1-p2)  │ (hub 1-p3)  │ (hub 1-p4)  │ (hub 1-p5)
  │
  ├─ Device 6  ├─ Device 7  ├─ Device 8  ├─ Device 9  ├─ Device 10
  │ (hub 1-p6)  │ (hub 1-p7)  │ (hub 1-p8)  │ (hub 1-p9)  │ (hub 1-p10)

USB Hub 2 (10 devices):
  ┌─ Device 11 ┌─ Device 12 ┌─ Device 13 ┌─ Device 14 ┌─ Device 15
  │ (hub 2-p1)  │ (hub 2-p2)  │ (hub 2-p3)  │ (hub 2-p4)  │ (hub 2-p5)
  │
  ├─ Device 16 ├─ Device 17 ├─ Device 18 ├─ Device 19 ├─ Device 20
  │ (hub 2-p6)  │ (hub 2-p7)  │ (hub 2-p8)  │ (hub 2-p9)  │ (hub 2-p10)

Air circulation: Fans between rows, prevent overheating
Power: Each hub has separate 12V adapter
```

### Load Distribution Algorithm

```
When allocating device for task:

1. Current Load Check:
   • Get current_queue_size for all 20 devices
   • Exclude offline/slow devices
   
2. Pick Least Busy:
   • device_with_min_queue_size = min(available_devices)
   • If tie: pick device with oldest last_activity (idle longest)
   
3. Allocation:
   • Add task to that device's queue
   • Max concurrent: 3 devices at a time
   • Others wait in FIFO queue
   
4. Fairness:
   • Over time, each device gets equal work
   • No single device overloaded
   • Automatic scaling: if device slow → other devices pick up
   
Example:
  Device 1: queue_size=2, last_activity=2 min ago
  Device 2: queue_size=0, last_activity=15 min ago  ← PICK THIS
  Device 3: queue_size=1, last_activity=5 min ago
  
  Task allocated to Device 2 (idle longest).
```

---

## Device Health Monitoring

### Health Check Protocol (Every 30 seconds)

```
For each device:

1. Ping Test:
   adb -s {device_id} shell "echo ok"
   Timeout: 5 sec
   
   If success:
     • Device status = "ok"
     • Log: "Device {id} healthy"
     
   If timeout:
     • Try reconnect (3 attempts, 2 sec delay)
     • If still fails: device status = "offline"
     • Log: "Device {id} offline, reason: timeout"

2. Battery Check:
   adb -s {device_id} shell "dumpsys battery | grep level"
   If < 15%: log warning, consider for maintenance

3. Message Count Check:
   Query SQLite: SELECT COUNT(*) FROM tasks WHERE device_id AND created_at TODAY
   If >= 30: device has hit daily limit, skip new tasks

4. Error Rate Check:
   If error_count > 5 in last hour:
     • Device status = "slow"
     • Increase timeout from 5 sec → 10 sec
     • Warning to user: "Device slow, may retry"

5. Memory Check (optional):
   adb -s {device_id} shell "dumpsys meminfo | grep TOTAL"
   If < 500 MB free: log warning, may restart device
```

### Automatic Recovery

```
If device status = "offline":

1. First attempt (immediately):
   adb disconnect {device_id}
   wait 1 sec
   adb connect {device_ip}:5555 (or use USB)
   wait 2 sec
   ping device
   
2. Second attempt (after 5 min):
   If still offline, try again
   
3. Third attempt (after 15 min):
   If still offline, give up for now
   Mark device: "maintenance_needed"
   Notify user in Telegram: "Device-05 offline, needs manual check"
   
4. Manual Recovery:
   User sees in Dashboard: Device offline
   User clicks "Reconnect" button
   → Triggers reconnect script
   → If success: device back online
   → If fail: user manually checks USB cable
```

---

## Performance Characteristics Per Device

### CPU & Memory During Execution

```
Idle state:
  • CPU: 5-10% (system background tasks)
  • RAM: 2-3 GB used
  • Storage: 50 GB free (of 128 GB)
  • Battery: 5% drain per hour
  
Active (sending message):
  • CPU: 60-80% (UIAutomator, ADB commands)
  • RAM: 4-5 GB used
  • Battery: 15-20% drain per hour
  
Waiting in queue:
  • CPU: 5% (minimal)
  • Battery: 3% drain per hour
  • Can leave screen OFF (saves 5% per hour)
```

### Thermal Management

```
Operating temperature: 35-45°C (normal)
Thermal throttle: Above 50°C
Shutdown: Above 60°C (safety cutoff)

During 60-70 sec message send:
  • Temperature rise: +5-10°C
  • Peak: ~45°C (safe)
  • Cool down: 2-3 minutes (before next task)
  
Rate limit enforcement:
  • Max 30 messages/day per device
  • = ~15 minutes of active execution
  • = Plenty of cooling time
  • Devices never overheat
```

---

## Device Maintenance Schedule

### Daily Checks (Automated, every 30 sec)

```
✅ Connection status (ADB ping)
✅ Battery level
✅ Error count
✅ Message counter (for rate limits)
✅ Temperature (optional)
```

### Weekly Maintenance (Manual, every Sunday)

```
For each device:
  1. Clear app cache (MAX, WhatsApp, SMS)
  2. Restart device
  3. Check for app updates
  4. Re-verify ADB connection
  5. Test send 1 message (sanity check)
  
Time per device: 5 minutes
Total time for 20 devices: ~100 minutes (1.5 hours)
```

### Monthly Maintenance (Quarterly)

```
Every 3 months:
  1. Update Android OS (if available)
  2. Update apps (MAX, WhatsApp, Google Play Services)
  3. Factory reset USB connections (reconnect all cables)
  4. Re-test all UIAutomator paths
  5. Full health check run
  
Time per device: 10-15 minutes
Total time for 20 devices: 200-300 minutes (3.5-5 hours)
```

---

## Device Failure Scenarios & Recovery

### Scenario 1: USB Cable Loose

```
Symptom: Device offline every 30 minutes
Root cause: Cable not fully inserted

Prevention:
  • Use cable locks (velcro ties)
  • Label cables (which device they go to)
  • Color-code hubs (Hub 1 red cables, Hub 2 blue cables)

Detection:
  • ADB ping fails 3x in a row
  • Notification: "Device offline, check USB cable"

Recovery:
  1. User clicks "Reconnect" in Dashboard
  2. Backend tries: adb reconnect
  3. If fails: TCP fallback
  4. If still fails: notify user "Check device {id} USB cable"
  5. User manually checks & re-seats cable
  6. Click "Reconnect" again
```

### Scenario 2: Device Crashes During Send

```
Symptom: Task hangs at "type_message" step
Root cause: App crashed

Detection:
  • ADB command timeout (30 sec, no response)
  • ADB connection drops
  
Recovery:
  1. Immediately timeout task (mark as failed)
  2. Close app: adb shell am kill com.alibaba.mobileim
  3. Device reboots (auto-recovery)
  4. Wait 10 sec for reboot
  5. Try reconnect (3 attempts)
  6. If success: device back online, task requeued to different device
  7. If fail: mark device offline, notify user
```

### Scenario 3: Notion Sync Fails for This Device

```
Symptom: Device sent message, but Notion not updated
Root cause: Network delay, Notion API timeout

Detection:
  • Task status = "sent", but notion_updated = false
  • Retry timer (check every 5 min)
  
Recovery:
  1. Task waits 5 minutes
  2. Retry NotionSync.update_status(task_id)
  3. If success: notion_updated = true
  4. If fail again: wait 10 min, retry again
  5. Max 3 retries, then mark as "sync_pending"
  6. Manual retry via Dashboard or next polling cycle
```

### Scenario 4: Device Battery Critical

```
Symptom: Battery < 15%
Detection: Health check sees battery_level < 15

Action:
  1. Stop assigning new tasks to this device
  2. Finish current task (if running)
  3. Mark device: "needs_charging"
  4. Notification: "Device-05 needs charging"
  
Recovery:
  User plugs in charger
  Wait 30 minutes for charging
  Mark device "ok" when battery > 50%
```

---

## USB Hub Redundancy & Failover

### Single Hub Failure

```
If entire Hub 1 goes offline:
  • Devices 1-10 all offline
  • Devices 11-20 still working
  • Backend detects all 10 devices offline
  • Notification: "Hub 1 offline"
  
Recovery:
  1. User replaces failed hub with identical ORICO model
  2. Re-seat all 10 USB cables
  3. Reboot hub (unplug power for 30 sec)
  4. Click "Reconnect All" in Dashboard
  5. Backend re-discovers devices
  6. Devices come back online (1-2 min)
  7. Tasks resume
```

### Daisy Chain Cable Failure

```
If daisy-chain between two hubs fails:
  • Hub 1: still working (direct to Mac)
  • Hub 2: offline (no power/data from daisy-chain)
  
Recovery:
  1. Replace daisy-chain cable (cheap, $5)
  2. Reboot both hubs
  3. Devices come back online
```

---

## Power Management

### Power Supply

```
Per USB Hub:
  • 12V/2A external power adapter
  • Two hubs = Two adapters (redundant)
  • Daisy-chaining: Both powered independently
  • Failure mode: One hub fails, other still works
  
Devices (via USB):
  • 5V power from USB 3.0 (from hub)
  • Can charge devices while running (slow charge)
  • Daytime: Run on USB power (charge + usage)
  • Nighttime: Plug into wall chargers (fast charge for next day)
```

### Power Consumption

```
Per device:
  • Idle: 1W
  • Active: 5W (during message send)
  • Charging: 10W (when plugged into wall)
  
20 devices idle: 20W
20 devices active (3 concurrent): 15W + 35W = 50W
Two USB hubs: 10W each = 20W
Total system power: 50W idle, 70W active

= Very efficient, can run on single USB power cable to Mac
```

---

## Monitoring Dashboard (Device Status)

### Per-Device Card Shows

```
Device #1
├─ Status: ✅ OK (green)
├─ Battery: 87% 🔋
├─ Temperature: 42°C 🌡️
├─ Messages today: 5/30
├─ Last activity: 2 minutes ago
├─ Current task: "Send to Ivan Petrov" (60% done)
├─ Error count: 0
├─ ADB Port: 5555
└─ Actions: [Reconnect] [Test] [View Logs] [Manual Override]
```

### Fleet Summary Shows

```
Fleet Status:
├─ Total devices: 20
├─ Online: 18 ✅
├─ Offline: 2 ⚠️
├─ Slow: 1 🐢
├─ Concurrent tasks: 3/3
├─ Queue pending: 12 tasks
├─ Messages sent today: 45/600
└─ System health: 90% 📊
```

---

## End of 13_DEVICE_TOPOLOGY_LOCAL.md

Полная топология 20 устройств + USB hub (ТОЛЬКО ЛОКАЛЬНО).

Готов создать **файл 14 (Security & Compliance)**?
