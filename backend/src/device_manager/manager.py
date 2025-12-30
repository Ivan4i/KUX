"""Device Manager - manages all Android devices"""

import asyncio
import yaml
from typing import Dict, List, Optional
from pathlib import Path
from loguru import logger

from .device import Device
from ..config import get_settings


class DeviceManager:
    """Manages all Google Pixel devices"""

    def __init__(self):
        """Initialize Device Manager"""
        self.devices: Dict[str, Device] = {}
        self.settings = get_settings()
        self._monitoring_task: Optional[asyncio.Task] = None
        self._initial_connect_task: Optional[asyncio.Task] = None

    async def initialize(self):
        """
        Initialize all devices from configuration

        Loads device configuration from devices.yaml and connects to each device
        """
        logger.info("🔧 Initializing Device Manager...")

        # Load device configuration
        config_path = Path(__file__).parent.parent.parent.parent / self.settings.device_config_path
        logger.info(f"📁 Loading device config from: {config_path}")

        if not config_path.exists():
            logger.error(f"❌ Device config file not found: {config_path}")
            return

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        devices_config = config.get('devices', [])
        logger.info(f"📱 Found {len(devices_config)} devices in config")

        # Create Device instances
        for device_config in devices_config:
            device = Device(
                device_id=device_config['id'],
                name=device_config['name'],
                location=device_config['location'],
                timezone=device_config['timezone'],
                tailscale_ip=device_config.get('tailscale_ip', ''),
                adb_port=device_config.get('adb_port', 5555),
                active_hours=device_config.get('active_hours', '08:00-22:00'),
                max_tasks_per_day=device_config.get('max_tasks_per_day', 50),
                adb_id=device_config.get('adb_id'),
                connection_type=device_config.get('connection_type', 'tailscale')
            )

            self.devices[device.device_id] = device
            connection_info = device.adb_id if device.connection_type == "usb" else device.tailscale_ip
            logger.info(f"  ✅ Registered device: {device.name} ({device.device_id}) - {device.connection_type.upper()} ({connection_info})")

        # Start health monitoring (handles reconnects for offline devices)
        logger.info("💓 Starting health monitoring...")
        self._monitoring_task = asyncio.create_task(self._health_monitoring_loop())

        # Connect to devices in BACKGROUND (non-blocking startup)
        logger.info("🔌 Starting device connection in background...")
        self._initial_connect_task = asyncio.create_task(self._connect_all_devices())

        logger.success("✅ Device Manager initialized (device connection in progress)!")

    async def shutdown(self):
        """Shutdown Device Manager and disconnect all devices"""
        logger.info("🛑 Shutting down Device Manager...")

        # Stop monitoring
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass

        # Stop initial connection task if still running
        if self._initial_connect_task:
            self._initial_connect_task.cancel()
            try:
                await self._initial_connect_task
            except asyncio.CancelledError:
                pass

        # Disconnect all devices
        for device in self.devices.values():
            await device.disconnect()

        logger.info("✅ Device Manager shut down")

    async def _connect_all_devices(self):
        """Connect to all configured devices"""
        tasks = []
        for device in self.devices.values():
            tasks.append(device.connect())

        results = await asyncio.gather(*tasks, return_exceptions=True)

        success_count = sum(1 for r in results if r is True)
        logger.info(f"📊 Connected {success_count}/{len(self.devices)} devices")

    async def _health_monitoring_loop(self):
        """Background task to monitor device health and auto-reconnect"""
        while True:
            try:
                # Wait 30 seconds between checks
                await asyncio.sleep(30)

                # Update status for all devices
                for device in self.devices.values():
                    try:
                        await device.update_status()

                        # Check for warnings
                        if device.current_status == "overheating":
                            logger.warning(f"🔥 {device.name} is overheating: {device.temperature}°C")
                        elif device.current_status == "low_battery":
                            logger.warning(f"🔋 {device.name} has low battery: {device.battery_level}%")
                        elif device.current_status == "offline":
                            logger.warning(f"📴 {device.name} is offline - attempting reconnect...")
                            # Try to reconnect (will scan for new port if needed)
                            success = await device.reconnect()
                            if success:
                                logger.success(f"✅ {device.name} reconnected successfully!")
                            else:
                                logger.error(f"❌ {device.name} reconnect failed")

                    except Exception as e:
                        logger.error(f"Error updating status for {device.device_id}: {e}")

            except asyncio.CancelledError:
                logger.info("Health monitoring loop cancelled")
                break
            except Exception as e:
                logger.error(f"Error in health monitoring loop: {e}")
                await asyncio.sleep(5)  # Short wait before retrying

    def get_device(self, device_id: str) -> Optional[Device]:
        """
        Get device by ID

        Args:
            device_id: Device identifier

        Returns:
            Device: Device instance, or None if not found
        """
        return self.devices.get(device_id)

    def get_all_devices(self) -> List[Device]:
        """Get list of all devices"""
        return list(self.devices.values())

    def get_device_status(self, device_id: str) -> Optional[Dict]:
        """Get status for specific device"""
        device = self.get_device(device_id)
        return device.get_status() if device else None

    def get_all_statuses(self) -> List[Dict]:
        """Get statuses for all devices"""
        return [device.get_status() for device in self.devices.values()]

    def get_available_device(self) -> Optional[Device]:
        """
        Get first available device for a new task

        Returns:
            Device: Available device, or None if no devices available
        """
        for device in self.devices.values():
            if device.is_available_for_task():
                return device

        logger.warning("No devices available for new task")
        return None

    async def assign_task_to_device(self, device_id: str, task_id: str) -> bool:
        """
        Assign a task to a specific device

        Args:
            device_id: Device identifier
            task_id: Task identifier

        Returns:
            bool: True if assigned successfully
        """
        device = self.get_device(device_id)

        if not device:
            logger.error(f"Device not found: {device_id}")
            return False

        if not device.is_available_for_task():
            logger.warning(f"Device {device_id} is not available (status: {device.current_status})")
            return False

        device.increment_active_tasks()
        logger.info(f"✅ Assigned task {task_id} to {device.name}")

        return True

    async def release_device(self, device_id: str, task_id: str):
        """
        Release device after task completion

        Args:
            device_id: Device identifier
            task_id: Task identifier
        """
        device = self.get_device(device_id)

        if device:
            device.decrement_active_tasks()
            logger.info(f"✅ Released {device.name} after task {task_id}")


# Global DeviceManager instance
device_manager = DeviceManager()
