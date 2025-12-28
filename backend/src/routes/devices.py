"""Devices API Routes"""

import subprocess
import asyncio
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from loguru import logger

from ..database.db import get_db
from ..database.schemas import DeviceStatus
from ..device_manager.manager import device_manager

router = APIRouter(prefix="/api/devices", tags=["devices"])


@router.get(
    "/",
    response_model=List[DeviceStatus],
    summary="List all devices",
    description="Retrieve status information for all registered Android devices",
    response_description="Array of device status objects with current metrics"
)
async def get_all_devices(db: Session = Depends(get_db)):
    """
    Get status information for all registered devices

    This endpoint returns real-time status for all Android devices managed by the platform.
    Each device status includes battery level, temperature, memory usage, and active task count.

    **Use Cases:**
    - Dashboard overview display
    - Device health monitoring
    - Load balancing decisions
    - System health checks

    **Device Status Fields:**
    - **id**: Unique device identifier (e.g., "pixel-th-1")
    - **name**: Human-readable device name
    - **current_status**: One of: online, offline, busy, sleeping, overheating, low_battery
    - **battery_level**: Battery percentage (0-100)
    - **temperature**: Device temperature in Celsius
    - **memory_usage**: Memory usage percentage (0-100)
    - **active_tasks**: Number of currently running tasks (0-10)
    - **last_heartbeat**: Timestamp of last successful device ping

    **Returns:**
    Array of DeviceStatus objects, sorted by device ID

    **Example Request:**
    ```
    GET /api/devices
    ```

    **Example Response:**
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
        },
        {
            "id": "pixel-th-2",
            "name": "Pixel 5 - Thailand Device 2",
            "current_status": "busy",
            "battery_level": 92,
            "temperature": 35.2,
            "memory_usage": 68,
            "active_tasks": 1,
            "last_heartbeat": "2025-12-04T10:29:55Z"
        }
    ]
    ```

    **Errors:**
    - **500**: Device Manager error or ADB connection failure

    **Note:**
    - Device status is cached and updated every 60 seconds by health monitoring
    - Offline devices will still appear in results with last known status
    - Temperature warnings trigger at >40°C, critical at >45°C
    """
    try:
        logger.info("📋 API: Getting all devices...")

        devices_status = []

        for device_id, device in device_manager.devices.items():
            status = device.get_status()
            devices_status.append(status)

        logger.success(f"✅ API: Returned {len(devices_status)} devices")
        return devices_status

    except Exception as e:
        logger.error(f"❌ API error getting devices: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{device_id}/status",
    response_model=DeviceStatus,
    summary="Get device status",
    description="Retrieve current status information for a specific device",
    response_description="Device status object with real-time metrics"
)
async def get_device_status(device_id: str, db: Session = Depends(get_db)):
    """
    Get real-time status for a specific device

    This endpoint returns current status information for a single device,
    including battery level, temperature, memory usage, and task activity.

    **Use Cases:**
    - Device detail view
    - Pre-task assignment health check
    - Troubleshooting device issues
    - Real-time monitoring dashboard

    **Args:**
    - **device_id** (str): Unique device identifier
      - Format: "pixel-th-1", "pixel-th-2", "pixel-th-3"
      - Must match a device configured in devices.yaml

    **Returns:**
    DeviceStatus object with current metrics

    **Example Request:**
    ```
    GET /api/devices/pixel-th-1/status
    ```

    **Example Success Response:**
    ```json
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
    ```

    **Status Values Explained:**
    - **online**: Device is connected and ready for tasks
    - **offline**: Device not reachable via ADB
    - **busy**: Device is currently executing a task
    - **sleeping**: Device cooling down after intensive work
    - **overheating**: Temperature >45°C, tasks blocked
    - **low_battery**: Battery <20%, tasks may be blocked

    **Errors:**
    - **404**: Device not found in configuration
    - **500**: ADB connection error or device communication failure

    **Note:**
    - Status is fetched from cache (updated every 60s by health monitor)
    - For real-time status, use the /refresh endpoint instead
    - Offline devices return last known status with stale timestamp
    """
    try:
        logger.info(f"📋 API: Getting device status for {device_id}...")

        device = device_manager.devices.get(device_id)

        if not device:
            logger.warning(f"⚠️ Device not found: {device_id}")
            raise HTTPException(status_code=404, detail=f"Device not found: {device_id}")

        status = device.get_status()

        logger.success(f"✅ API: Returned status for {device_id}")
        return status

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ API error getting device status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/{device_id}/refresh",
    summary="Refresh device status",
    description="Force an immediate status update for a specific device",
    response_description="Updated device status with fresh metrics"
)
async def refresh_device_status(device_id: str, db: Session = Depends(get_db)):
    """
    Force immediate status refresh for a device

    This endpoint bypasses the cached status and forces an immediate query
    to the device via ADB to get real-time metrics. Useful when you need
    up-to-the-second information before making critical decisions.

    **Use Cases:**
    - Pre-task validation (check device is truly ready)
    - Troubleshooting (verify device is responding)
    - Manual health check after suspected issues
    - Admin dashboard manual refresh

    **Process:**
    1. Connects to device via ADB over Tailscale
    2. Queries battery level, temperature, memory usage
    3. Updates cached status in Device Manager
    4. Returns fresh status to client

    **Args:**
    - **device_id** (str): Device ID to refresh (e.g., "pixel-th-1")

    **Returns:**
    DeviceStatus object with freshly queried metrics

    **Example Request:**
    ```
    POST /api/devices/pixel-th-1/refresh
    ```

    **Example Response:**
    ```json
    {
        "id": "pixel-th-1",
        "name": "Pixel 5 - Thailand Device 1",
        "current_status": "online",
        "battery_level": 86,
        "temperature": 33.1,
        "memory_usage": 47,
        "active_tasks": 0,
        "last_heartbeat": "2025-12-04T10:35:22Z"
    }
    ```

    **Errors:**
    - **404**: Device not found in configuration
    - **500**: ADB connection failed or device not responding

    **Performance:**
    - Typical response time: 2-5 seconds (includes ADB queries)
    - Avoid excessive calls (rate limited to prevent device strain)
    - Use cached status endpoint for frequent polling

    **Note:**
    - This is a synchronous operation that queries the device immediately
    - May timeout if device is unresponsive (30s timeout)
    - Updates the health monitoring cache with fresh data
    """
    try:
        logger.info(f"🔄 API: Refreshing device status for {device_id}...")

        device = device_manager.devices.get(device_id)

        if not device:
            raise HTTPException(status_code=404, detail=f"Device not found: {device_id}")

        # Force status update
        await device.update_status()

        status = device.get_status()

        logger.success(f"✅ API: Refreshed status for {device_id}")
        return status

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ API error refreshing device: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/{device_id}/reboot",
    summary="Reboot device",
    description="Remotely reboot an Android device via ADB",
    response_description="Reboot confirmation message"
)
async def reboot_device(device_id: str, db: Session = Depends(get_db)):
    """
    Remotely reboot an Android device

    This endpoint triggers a full device reboot via ADB. The device will
    restart and reconnect to Tailscale VPN automatically. Useful for
    recovery scenarios, clearing stuck processes, or scheduled maintenance.

    **Use Cases:**
    - Level 4 recovery (after app restart fails)
    - Clear device memory/cache
    - Scheduled maintenance reboots
    - Manual troubleshooting by admin
    - Device stuck in abnormal state

    **Process:**
    1. Validates device exists in configuration
    2. Sends ADB reboot command over Tailscale
    3. Device begins reboot (takes ~60-90 seconds)
    4. Device automatically reconnects to Tailscale on boot
    5. Health monitoring detects reconnection

    **Args:**
    - **device_id** (str): Device ID to reboot (e.g., "pixel-th-1")

    **Returns:**
    Success confirmation object

    **Example Request:**
    ```
    POST /api/devices/pixel-th-1/reboot
    ```

    **Example Response:**
    ```json
    {
        "success": true,
        "message": "Device pixel-th-1 is rebooting",
        "device_id": "pixel-th-1"
    }
    ```

    **Errors:**
    - **404**: Device not found in configuration
    - **500**: ADB reboot command failed or device not responding

    **Important Notes:**
    - Device will be offline for 60-90 seconds during reboot
    - Any running tasks on the device will fail
    - Device status will show "offline" until reboot completes
    - Tailscale should auto-reconnect on boot (verify config)
    - Health monitoring will auto-detect when device comes back online

    **Recovery Timeline:**
    - T+0s: Reboot command sent
    - T+5s: Device shuts down
    - T+30s: Device boots up, Tailscale starts
    - T+60s: Device connects to Tailscale
    - T+90s: Health monitoring detects device online

    **Warning:**
    - Do not reboot multiple devices simultaneously
    - Ensure Tailscale is configured to start on boot
    - Wait at least 2 minutes before considering reboot failed
    """
    try:
        logger.info(f"🔄 API: Rebooting device {device_id}...")

        device = device_manager.devices.get(device_id)

        if not device:
            raise HTTPException(status_code=404, detail=f"Device not found: {device_id}")

        # Reboot device
        success = await device.adb.reboot()

        if not success:
            raise HTTPException(status_code=500, detail="Failed to reboot device")

        logger.success(f"✅ API: Device {device_id} rebooting...")
        return {
            "success": True,
            "message": f"Device {device_id} is rebooting",
            "device_id": device_id
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ API error rebooting device: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{device_id}/screenshot",
    summary="Capture device screenshot",
    description="Take a screenshot of the device's current screen via ADB",
    response_description="Screenshot capture result with file path"
)
async def take_device_screenshot(device_id: str, db: Session = Depends(get_db)):
    """
    Capture screenshot of device's current screen

    This endpoint remotely captures a screenshot of the Android device's
    current display via ADB. Screenshots are saved to the backend's
    screenshots directory and can be used for debugging, verification,
    and logging purposes.

    **Use Cases:**
    - Verify WhatsApp message sent successfully
    - Debug UI automation issues
    - Capture proof of delivery
    - Manual inspection of device state
    - Error documentation (attach to logs)
    - Recovery agent decision-making

    **Process:**
    1. Validates device exists and is online
    2. Executes ADB screencap command via Tailscale
    3. Pulls screenshot file from device to backend
    4. Saves to `/backend/data/screenshots/{device_id}/`
    5. Returns local file path

    **Args:**
    - **device_id** (str): Device ID to capture (e.g., "pixel-th-1")

    **Returns:**
    Screenshot result object with file path

    **Example Request:**
    ```
    GET /api/devices/pixel-th-1/screenshot
    ```

    **Example Response:**
    ```json
    {
        "success": true,
        "device_id": "pixel-th-1",
        "screenshot_path": "/backend/data/screenshots/pixel-th-1/screenshot_20251204_103022.png"
    }
    ```

    **Screenshot Naming:**
    - Format: `screenshot_{timestamp}.png`
    - Example: `screenshot_20251204_103022.png`
    - Stored in: `/backend/data/screenshots/{device_id}/`
    - Retention: 7 days (auto-cleanup)

    **Errors:**
    - **404**: Device not found in configuration
    - **500**: ADB screencap failed or device not responding
    - **500**: File transfer failed (check disk space)

    **Performance:**
    - Typical response time: 2-4 seconds
    - File size: ~200KB - 2MB (depending on screen resolution)
    - Resolution: 1080x2340 (Google Pixel 5 native)

    **Important Notes:**
    - Screenshots contain PII (phone numbers, messages) - handle securely
    - Old screenshots auto-deleted after 7 days
    - Fails if device screen is off (wake device first)
    - Requires ~5MB free space on backend
    - Not real-time (2-4 second delay typical)

    **Use in Automation:**
    ```python
    # Example: Verify message sent
    result = await whatsapp_agent.send_message(...)
    if result["success"]:
        screenshot = await device.adb.take_screenshot()
        # Attach screenshot to log
    ```

    **File Cleanup:**
    - Screenshots older than 7 days deleted automatically
    - Manual cleanup: DELETE /api/logs/cleanup (cleans logs + screenshots)
    - Check disk usage: GET /api/devices/{device_id}/status (memory_usage)
    """
    try:
        logger.info(f"📸 API: Taking screenshot of {device_id}...")

        device = device_manager.devices.get(device_id)

        if not device:
            raise HTTPException(status_code=404, detail=f"Device not found: {device_id}")

        screenshot_path = await device.adb.take_screenshot()

        if not screenshot_path:
            raise HTTPException(status_code=500, detail="Failed to take screenshot")

        logger.success(f"✅ API: Screenshot taken for {device_id}")
        return {
            "success": True,
            "device_id": device_id,
            "screenshot_path": screenshot_path
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ API error taking screenshot: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/{device_id}/scrcpy",
    summary="Launch scrcpy for device",
    description="Launch scrcpy screen mirroring for a specific device"
)
async def launch_scrcpy(device_id: str, db: Session = Depends(get_db)):
    """
    Launch scrcpy to mirror device screen

    Opens a scrcpy window for real-time screen mirroring and remote control.
    Requires scrcpy to be installed on the server machine.
    """
    try:
        logger.info(f"🖥️ API: Launching scrcpy for {device_id}...")

        device = device_manager.devices.get(device_id)

        if not device:
            raise HTTPException(status_code=404, detail=f"Device not found: {device_id}")

        # Get ADB ID for scrcpy
        adb_id = device.adb_id or ""
        device_name = device.name or device_id

        if not adb_id:
            raise HTTPException(status_code=400, detail="Device ADB ID not configured")

        # Launch scrcpy in background
        cmd = [
            "scrcpy",
            "-s", adb_id,
            "--window-title", device_name,
            "--max-size", "1024"
        ]

        # Run scrcpy as detached process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )

        logger.success(f"✅ API: scrcpy launched for {device_id} (PID: {process.pid})")
        return {
            "success": True,
            "message": f"scrcpy launched for {device_name}",
            "device_id": device_id,
            "pid": process.pid
        }

    except HTTPException:
        raise
    except FileNotFoundError:
        logger.error("❌ scrcpy not found. Install with: brew install scrcpy")
        raise HTTPException(status_code=500, detail="scrcpy not installed on server")
    except Exception as e:
        logger.error(f"❌ API error launching scrcpy: {e}")
        raise HTTPException(status_code=500, detail=str(e))
