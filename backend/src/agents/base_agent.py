"""Base Agent - Abstract base class for all platform agents"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
from datetime import datetime
from loguru import logger

from ..device_manager.device import Device


class BaseAgent(ABC):
    """Abstract base class for platform agents (WhatsApp, LinkedIn, Instagram)"""

    def __init__(self, platform_name: str):
        """
        Initialize Base Agent

        Args:
            platform_name: Name of the platform (e.g., "WhatsApp", "LinkedIn")
        """
        self.platform_name = platform_name
        self.last_action_time: Optional[datetime] = None
        self.action_count: int = 0

    @abstractmethod
    async def send_message(
        self,
        device: Device,
        recipient: str,
        message: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send a message to a recipient

        Args:
            device: Device instance to use
            recipient: Recipient identifier (phone number, username, etc.)
            message: Message content
            **kwargs: Platform-specific parameters

        Returns:
            dict: Result with success status and metadata
        """
        pass

    @abstractmethod
    async def verify_app_state(self, device: Device) -> Dict[str, Any]:
        """
        Verify that the app is in correct state

        Args:
            device: Device instance

        Returns:
            dict: App state information
        """
        pass

    @abstractmethod
    async def open_app(self, device: Device) -> bool:
        """
        Open the platform app

        Args:
            device: Device instance

        Returns:
            bool: True if successful
        """
        pass

    @abstractmethod
    async def close_app(self, device: Device) -> bool:
        """
        Close the platform app

        Args:
            device: Device instance

        Returns:
            bool: True if successful
        """
        pass

    async def restart_app(self, device: Device) -> bool:
        """
        Restart the platform app

        Args:
            device: Device instance

        Returns:
            bool: True if successful
        """
        try:
            logger.info(f"Restarting {self.platform_name} app...")

            # Close app
            await self.close_app(device)

            # Wait before reopening
            import asyncio
            await asyncio.sleep(2)

            # Open app
            success = await self.open_app(device)

            if success:
                logger.success(f"✅ {self.platform_name} app restarted")
            else:
                logger.error(f"❌ Failed to restart {self.platform_name} app")

            return success

        except Exception as e:
            logger.error(f"Error restarting {self.platform_name} app: {e}")
            return False

    def _update_action_metrics(self):
        """Update action metrics (called after each action)"""
        self.last_action_time = datetime.utcnow()
        self.action_count += 1

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get agent metrics

        Returns:
            dict: Metrics data
        """
        return {
            "platform": self.platform_name,
            "action_count": self.action_count,
            "last_action": self.last_action_time.isoformat() if self.last_action_time else None
        }

    async def take_screenshot(self, device: Device, reason: str = "") -> Optional[str]:
        """
        Take screenshot for debugging/analysis

        Args:
            device: Device instance
            reason: Reason for screenshot

        Returns:
            str: Screenshot path, or None if failed
        """
        try:
            screenshot_path = await device.adb.take_screenshot()

            if screenshot_path:
                logger.debug(f"📸 Screenshot saved: {screenshot_path} ({reason})")
            else:
                logger.warning("⚠️ Failed to take screenshot")

            return screenshot_path

        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return None

    async def analyze_current_screen(
        self,
        device: Device,
        analysis_type: str = "ui_elements"
    ) -> Optional[Dict]:
        """
        Analyze current screen using LLM

        Args:
            device: Device instance
            analysis_type: Type of analysis

        Returns:
            dict: Analysis results
        """
        try:
            from ..integrations.puter_client import puter_client

            # Take screenshot
            screenshot_path = await self.take_screenshot(device, reason=f"analysis:{analysis_type}")

            if not screenshot_path:
                return None

            # Analyze with LLM
            analysis = await puter_client.analyze_screenshot(
                screenshot_path=screenshot_path,
                analysis_type=analysis_type
            )

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing screen: {e}")
            return None
