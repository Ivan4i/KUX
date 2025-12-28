"""Device class - represents a single Google Pixel device"""

from typing import Optional, Dict, Any
from datetime import datetime
from loguru import logger

from .adb_handler import ADBHandler


class Device:
    """Represents a Google Pixel device"""

    def __init__(
        self,
        device_id: str,
        name: str,
        location: str,
        timezone: str,
        tailscale_ip: str,
        adb_port: int = 5555,
        active_hours: str = "08:00-22:00",
        max_tasks_per_day: int = 50,
        adb_id: str = None,
        connection_type: str = "tailscale"
    ):
        """
        Initialize device

        Args:
            device_id: Unique device identifier (e.g., "pixel-th-1" or "honor-1")
            name: Display name (e.g., "Pixel-TH-1" or "HONOR ALT-LX1")
            location: Location (e.g., "Bangkok, Thailand")
            timezone: Timezone (e.g., "Asia/Bangkok")
            tailscale_ip: Tailscale IP address (for network devices)
            adb_port: ADB port (default: 5555)
            active_hours: Active hours range (e.g., "08:00-22:00")
            max_tasks_per_day: Maximum tasks per day
            adb_id: ADB device ID for USB devices (e.g., "AHLFBB5111109330")
            connection_type: "usb" or "tailscale"
        """
        self.device_id = device_id
        self.id = device_id  # Alias for compatibility
        self.name = name
        self.location = location
        self.timezone = timezone
        self.tailscale_ip = tailscale_ip
        self.adb_port = adb_port
        self.active_hours = active_hours
        self.max_tasks_per_day = max_tasks_per_day
        self.adb_id = adb_id
        self.connection_type = connection_type

        # ADB handler
        self.adb = ADBHandler(device_id, tailscale_ip, adb_port, adb_id, connection_type)

        # Status tracking
        self.current_status = "offline"  # online, offline, sleeping, busy
        self.last_heartbeat: Optional[datetime] = None
        self.battery_level = 0
        self.temperature = 0.0
        self.memory_usage = 0
        self.active_tasks_count = 0

    async def connect(self) -> bool:
        """Connect to device via ADB"""
        success = await self.adb.connect()
        if success:
            self.current_status = "online"
            # Update port if it was found by scanning
            if self.adb.adb_port != self.adb_port:
                logger.info(f"📝 Port changed for {self.device_id}: {self.adb_port} -> {self.adb.adb_port}")
                self.adb_port = self.adb.adb_port
            await self.update_status()
        return success

    async def reconnect(self) -> bool:
        """Reconnect to device (used when connection is lost)"""
        logger.info(f"🔄 Attempting to reconnect to {self.device_id}...")
        await self.adb.disconnect()
        return await self.connect()

    async def disconnect(self) -> bool:
        """Disconnect from device"""
        success = await self.adb.disconnect()
        if success:
            self.current_status = "offline"
        return success

    async def update_status(self) -> Dict[str, Any]:
        """
        Update device status (battery, temperature, memory)

        Returns:
            dict: Updated status data
        """
        try:
            # Check if online
            is_online = await self.adb.is_online()

            if not is_online:
                self.current_status = "offline"
                return self.get_status()

            # Update metrics
            self.battery_level = await self.adb.get_battery_level()
            self.temperature = await self.adb.get_temperature()
            self.memory_usage = await self.adb.get_memory_usage()
            self.last_heartbeat = datetime.utcnow()

            # Determine status
            if self.active_tasks_count > 0:
                self.current_status = "busy"
            elif self.temperature > 40:
                self.current_status = "overheating"
            elif self.battery_level < 15:
                self.current_status = "low_battery"
            else:
                self.current_status = "online"

            logger.debug(f"Updated status for {self.device_id}: {self.current_status}")

            return self.get_status()

        except Exception as e:
            logger.error(f"Error updating status for {self.device_id}: {e}")
            self.current_status = "error"
            return self.get_status()

    def get_status(self) -> Dict[str, Any]:
        """
        Get current device status

        Returns:
            dict: Status data
        """
        return {
            "id": self.device_id,
            "name": self.name,
            "location": self.location,
            "timezone": self.timezone,
            "current_status": self.current_status,
            "battery_level": self.battery_level,
            "temperature": self.temperature,
            "memory_usage": self.memory_usage,
            "active_tasks": self.active_tasks_count,
            "last_heartbeat": self.last_heartbeat.isoformat() if self.last_heartbeat else None
        }

    async def take_screenshot(self, output_path: str) -> Optional[bytes]:
        """Take screenshot"""
        return await self.adb.take_screenshot(output_path)

    async def execute_shell(self, command: str) -> Optional[str]:
        """Execute shell command"""
        return await self.adb.shell_command(command)

    async def reboot(self) -> bool:
        """Reboot device"""
        logger.warning(f"Rebooting {self.device_id}...")
        return await self.adb.reboot()

    def is_available_for_task(self) -> bool:
        """
        Check if device is available for a new task

        Returns:
            bool: True if device can accept a new task
        """
        return (
            self.current_status == "online" and
            self.active_tasks_count == 0 and
            self.battery_level > 15 and
            self.temperature < 40
        )

    def increment_active_tasks(self):
        """Increment active task counter"""
        self.active_tasks_count += 1
        if self.active_tasks_count > 0:
            self.current_status = "busy"

    def decrement_active_tasks(self):
        """Decrement active task counter"""
        self.active_tasks_count = max(0, self.active_tasks_count - 1)
        if self.active_tasks_count == 0:
            self.current_status = "online"
