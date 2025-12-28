"""ADB command handler for Android devices"""

import subprocess
import asyncio
import socket
from typing import Optional, Dict, Any, List
from loguru import logger


class ADBHandler:
    """Handles ADB commands to Android devices"""

    def __init__(self, device_id: str, tailscale_ip: str, adb_port: int = 5555, adb_id: str = None, connection_type: str = "tailscale"):
        """
        Initialize ADB handler for a specific device

        Args:
            device_id: Device identifier (e.g., "pixel-th-1" or "honor-1")
            tailscale_ip: Tailscale IP address (for network devices)
            adb_port: ADB port (default: 5555)
            adb_id: ADB device ID for USB devices (e.g., "AHLFBB5111109330")
            connection_type: "usb" or "tailscale"
        """
        self.device_id = device_id
        self.tailscale_ip = tailscale_ip
        self.adb_port = adb_port
        self.adb_id = adb_id
        self.connection_type = connection_type

        # Set ADB address based on connection type
        if connection_type == "usb":
            self.adb_address = adb_id  # Use USB device ID directly
        else:
            self.adb_address = f"{tailscale_ip}:{adb_port}"  # Network address

        self.connected = False

    def _check_port_sync(self, port: int) -> bool:
        """Synchronously check if port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            result = sock.connect_ex((self.tailscale_ip, port))
            sock.close()
            return result == 0
        except:
            return False

    async def scan_adb_port(self) -> Optional[int]:
        """
        Scan for open ADB port on the device (Wireless Debugging uses dynamic ports)
        Uses parallel scanning for speed.

        Returns:
            int: Found port number, or None if not found
        """
        # Wireless debugging ports are typically in range 37000-45000
        port_ranges = [(37000, 45000), (30000, 37000), (45000, 50000)]

        logger.info(f"🔍 Scanning for ADB port on {self.tailscale_ip}...")

        loop = asyncio.get_event_loop()

        for start_port, end_port in port_ranges:
            logger.info(f"📡 Scanning ports {start_port}-{end_port}...")

            # Scan ports in parallel batches
            batch_size = 200
            for batch_start in range(start_port, end_port, batch_size):
                batch_end = min(batch_start + batch_size, end_port)
                ports = list(range(batch_start, batch_end))

                # Check ports in parallel using thread pool
                tasks = [loop.run_in_executor(None, self._check_port_sync, port) for port in ports]
                results = await asyncio.gather(*tasks)

                # Find open ports
                open_ports = [port for port, is_open in zip(ports, results) if is_open]

                for port in open_ports:
                    # Try ADB connect on open port
                    test_result = await self._execute_adb_command(f"connect {self.tailscale_ip}:{port}")
                    if test_result and ("connected" in test_result.lower() or "already connected" in test_result.lower()):
                        logger.success(f"✅ Found ADB on port {port}")
                        return port
                    else:
                        await self._execute_adb_command(f"disconnect {self.tailscale_ip}:{port}")

        logger.warning(f"⚠️ No ADB port found on {self.tailscale_ip}")
        return None

    async def connect(self) -> bool:
        """
        Connect to device via ADB

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # USB devices are already connected via cable - just verify
            if self.connection_type == "usb":
                logger.info(f"Verifying USB device {self.device_id} ({self.adb_address})...")

                # Check if device is visible in adb devices
                result = await self._execute_adb_command("devices")

                if result and self.adb_address in result:
                    self.connected = True
                    logger.success(f"✅ USB device {self.device_id} is connected")
                    return True
                else:
                    logger.error(f"❌ USB device {self.device_id} not found in adb devices")
                    return False

            # Network devices (Tailscale) - use adb connect
            else:
                logger.info(f"Connecting to {self.device_id} at {self.adb_address}...")

                # Execute adb connect command
                result = await self._execute_adb_command(f"connect {self.adb_address}")

                if result and ("connected" in result.lower() or "already connected" in result.lower()):
                    self.connected = True
                    logger.success(f"✅ Connected to {self.device_id}")
                    return True
                else:
                    # Connection failed - try to scan for new port
                    logger.warning(f"⚠️ Failed to connect on port {self.adb_port}, scanning for new port...")
                    new_port = await self.scan_adb_port()

                    if new_port:
                        # Update port and address
                        self.adb_port = new_port
                        self.adb_address = f"{self.tailscale_ip}:{new_port}"
                        self.connected = True
                        logger.success(f"✅ Connected to {self.device_id} on new port {new_port}")
                        return True
                    else:
                        logger.error(f"❌ Failed to connect to {self.device_id}: no ADB port found")
                        return False

        except Exception as e:
            logger.error(f"❌ Error connecting to {self.device_id}: {e}")
            return False

    async def disconnect(self) -> bool:
        """Disconnect from device"""
        try:
            result = await self._execute_adb_command(f"disconnect {self.adb_address}")
            self.connected = False
            logger.info(f"Disconnected from {self.device_id}")
            return True
        except Exception as e:
            logger.error(f"Error disconnecting from {self.device_id}: {e}")
            return False

    async def is_online(self) -> bool:
        """Check if device is online and responsive"""
        try:
            result = await self.shell_command("echo 'ping'")
            return result is not None and "ping" in result
        except:
            return False

    async def get_battery_level(self) -> int:
        """
        Get battery level (0-100)

        Returns:
            int: Battery percentage, or 0 if error
        """
        try:
            result = await self.shell_command("dumpsys battery")
            if result:
                # Find "level: XX" line specifically
                import re
                match = re.search(r'level:\s*(\d+)', result)
                if match:
                    return int(match.group(1))
            return 0
        except Exception as e:
            logger.error(f"Error getting battery level for {self.device_id}: {e}")
            return 0

    async def get_temperature(self) -> float:
        """
        Get device temperature in Celsius from battery info

        Returns:
            float: Temperature in Celsius, or 0.0 if error
        """
        try:
            # Use dumpsys battery which includes temperature (in tenths of degrees)
            result = await self.shell_command("dumpsys battery")
            if result:
                import re
                match = re.search(r'temperature:\s*(\d+)', result)
                if match:
                    # Temperature is in tenths of degrees (e.g., 280 = 28.0°C)
                    temp = int(match.group(1)) / 10.0
                    return round(temp, 1)
            return 0.0
        except Exception as e:
            logger.error(f"Error getting temperature for {self.device_id}: {e}")
            return 0.0

    async def get_memory_usage(self) -> int:
        """
        Get RAM usage percentage

        Returns:
            int: Memory usage percentage (0-100)
        """
        try:
            result = await self.shell_command("dumpsys meminfo | grep 'Total RAM'")
            if result:
                # Parse memory info
                # This is a simplified version - actual implementation would need more parsing
                return 60  # Placeholder
            return 0
        except Exception as e:
            logger.error(f"Error getting memory usage for {self.device_id}: {e}")
            return 0

    async def take_screenshot(self, output_path: str = "/tmp/screenshot.png") -> Optional[bytes]:
        """
        Take a screenshot and return as bytes

        Args:
            output_path: Local path to save screenshot

        Returns:
            bytes: Screenshot image data, or None if error
        """
        try:
            # Take screenshot on device
            await self.shell_command("screencap -p /sdcard/screenshot.png")

            # Pull screenshot from device
            await self._execute_adb_command(f"-s {self.adb_address} pull /sdcard/screenshot.png {output_path}")

            # Read screenshot file
            with open(output_path, 'rb') as f:
                screenshot_data = f.read()

            # Clean up
            await self.shell_command("rm /sdcard/screenshot.png")

            return screenshot_data

        except Exception as e:
            logger.error(f"Error taking screenshot for {self.device_id}: {e}")
            return None

    async def shell_command(self, command: str) -> Optional[str]:
        """
        Execute shell command on device

        Args:
            command: Shell command to execute

        Returns:
            str: Command output, or None if error
        """
        full_command = f"-s {self.adb_address} shell {command}"
        return await self._execute_adb_command(full_command)

    async def tap(self, x: int, y: int) -> bool:
        """
        Perform tap at coordinates

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            bool: True if successful
        """
        try:
            await self.shell_command(f"input tap {x} {y}")
            return True
        except:
            return False

    async def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300) -> bool:
        """
        Perform swipe gesture

        Args:
            x1, y1: Start coordinates
            x2, y2: End coordinates
            duration_ms: Swipe duration in milliseconds

        Returns:
            bool: True if successful
        """
        try:
            await self.shell_command(f"input swipe {x1} {y1} {x2} {y2} {duration_ms}")
            return True
        except:
            return False

    async def input_text(self, text: str) -> bool:
        """
        Input text (note: special characters need escaping)

        Args:
            text: Text to input

        Returns:
            bool: True if successful
        """
        try:
            # Escape special characters
            escaped_text = text.replace(" ", "%s")
            await self.shell_command(f"input text '{escaped_text}'")
            return True
        except:
            return False

    async def press_key(self, keycode: str) -> bool:
        """
        Press key (e.g., KEYCODE_BACK, KEYCODE_HOME)

        Args:
            keycode: Android keycode

        Returns:
            bool: True if successful
        """
        try:
            await self.shell_command(f"input keyevent {keycode}")
            return True
        except:
            return False

    async def start_app(self, package_name: str, activity: Optional[str] = None) -> bool:
        """
        Start an application

        Args:
            package_name: App package name (e.g., "com.whatsapp")
            activity: Activity to start (optional)

        Returns:
            bool: True if successful
        """
        try:
            if activity:
                command = f"am start -n {package_name}/{activity}"
            else:
                command = f"monkey -p {package_name} -c android.intent.category.LAUNCHER 1"

            await self.shell_command(command)
            return True
        except:
            return False

    async def reboot(self) -> bool:
        """Reboot device"""
        try:
            await self.shell_command("reboot")
            self.connected = False
            return True
        except:
            return False

    async def _execute_adb_command(self, command: str) -> Optional[str]:
        """
        Execute ADB command

        Args:
            command: ADB command (without 'adb' prefix)

        Returns:
            str: Command output, or None if error
        """
        try:
            full_command = f"adb {command}"

            # Execute command asynchronously
            process = await asyncio.create_subprocess_shell(
                full_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                return stdout.decode('utf-8').strip()
            else:
                logger.error(f"ADB command failed: {stderr.decode('utf-8')}")
                return None

        except Exception as e:
            logger.error(f"Error executing ADB command '{command}': {e}")
            return None
