"""Telegram Bot - sends alerts and notifications"""

import asyncio
from typing import Optional, List, Dict
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError
from loguru import logger

from ..config import get_settings


class TelegramBot:
    """Manages Telegram notifications and alerts"""

    def __init__(self):
        """Initialize Telegram Bot"""
        settings = get_settings()
        self.bot = Bot(token=settings.telegram_bot_token)
        self.chat_id = settings.telegram_chat_id  # Will be set in config
        self.enabled = True  # Can be disabled for testing

    async def send_alert(
        self,
        message: str,
        level: str = "INFO",
        data: Optional[Dict] = None
    ) -> bool:
        """
        Send alert message to Telegram

        Args:
            message: Alert message text
            level: Alert level (INFO, WARNING, ERROR)
            data: Optional additional data to include

        Returns:
            bool: True if sent successfully
        """
        if not self.enabled:
            logger.debug("Telegram bot disabled, skipping alert")
            return False

        try:
            # Format message with emoji based on level
            emoji_map = {
                "INFO": "ℹ️",
                "WARNING": "⚠️",
                "ERROR": "❌",
                "SUCCESS": "✅"
            }

            emoji = emoji_map.get(level, "📢")
            formatted_message = f"{emoji} **{level}**\n\n{message}"

            # Add data if provided
            if data:
                formatted_message += "\n\n**Details:**\n"
                for key, value in data.items():
                    formatted_message += f"• {key}: {value}\n"

            # Add timestamp
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            formatted_message += f"\n_Sent at: {timestamp}_"

            # Send message
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=formatted_message,
                parse_mode="Markdown"
            )

            logger.debug(f"📤 Sent {level} alert to Telegram")
            return True

        except TelegramError as e:
            logger.error(f"❌ Telegram error: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error sending Telegram alert: {e}")
            return False

    async def send_task_started(
        self,
        task_id: str,
        recipient_name: str,
        phone_number: str,
        device_name: str
    ) -> bool:
        """Send notification when task starts"""
        message = f"""📧 WhatsApp Task Started

**Recipient:** {recipient_name}
**Phone:** {phone_number}
**Device:** {device_name}
**Task ID:** {task_id}"""

        return await self.send_alert(message, level="INFO")

    async def send_task_completed(
        self,
        task_id: str,
        recipient_name: str,
        phone_number: str,
        device_name: str,
        duration_seconds: float
    ) -> bool:
        """Send notification when task completes successfully"""
        message = f"""✅ WhatsApp Message Sent

**Recipient:** {recipient_name}
**Phone:** {phone_number}
**Device:** {device_name}
**Duration:** {duration_seconds:.1f}s
**Task ID:** {task_id}"""

        return await self.send_alert(message, level="SUCCESS")

    async def send_task_failed(
        self,
        task_id: str,
        recipient_name: str,
        phone_number: str,
        device_name: str,
        error_message: str,
        attempt_count: int
    ) -> bool:
        """Send notification when task fails"""
        message = f"""❌ WhatsApp Task Failed

**Recipient:** {recipient_name}
**Phone:** {phone_number}
**Device:** {device_name}
**Error:** {error_message}
**Attempts:** {attempt_count}
**Task ID:** {task_id}"""

        return await self.send_alert(message, level="ERROR", data={
            "Next Action": "Will retry automatically" if attempt_count < 3 else "Manual intervention required"
        })

    async def send_device_alert(
        self,
        device_name: str,
        alert_type: str,
        alert_data: Dict
    ) -> bool:
        """Send device health alert"""
        alert_messages = {
            "battery_low": f"🔋 **Low Battery Warning**\n\nDevice: {device_name}\nBattery: {alert_data.get('battery_level')}%",
            "temperature_high": f"🔥 **High Temperature Warning**\n\nDevice: {device_name}\nTemperature: {alert_data.get('temperature')}°C",
            "offline": f"📴 **Device Offline**\n\nDevice: {device_name}\nLast seen: {alert_data.get('last_heartbeat')}",
            "connection_lost": f"🔌 **Connection Lost**\n\nDevice: {device_name}\nReason: {alert_data.get('reason', 'Unknown')}"
        }

        message = alert_messages.get(alert_type, f"⚠️ Device Alert: {alert_type}\n\nDevice: {device_name}")

        return await self.send_alert(message, level="WARNING", data=alert_data)

    async def send_daily_summary(
        self,
        summary_data: Dict
    ) -> bool:
        """Send daily summary report"""
        message = f"""📊 Daily Summary Report

**Date:** {summary_data.get('date', datetime.utcnow().strftime('%Y-%m-%d'))}

**Tasks:**
• Total: {summary_data.get('total_tasks', 0)}
• Completed: {summary_data.get('completed_tasks', 0)} ✅
• Failed: {summary_data.get('failed_tasks', 0)} ❌
• Pending: {summary_data.get('pending_tasks', 0)} ⏳

**Success Rate:** {summary_data.get('success_rate', 0):.1f}%

**Devices:**"""

        for device in summary_data.get('devices', []):
            message += f"\n• {device['name']}: {device['tasks_completed']} tasks"

        return await self.send_alert(message, level="INFO")

    async def send_recovery_prompt(
        self,
        task_id: str,
        error_message: str,
        suggested_action: str
    ) -> bool:
        """
        Send interactive recovery prompt (Slice 2 feature)

        Note: This requires Telegram Bot API with inline keyboards
        For Slice 1, we'll just send an informational message
        """
        message = f"""🔄 Recovery Action Needed

**Task ID:** {task_id}
**Error:** {error_message}
**Suggested Action:** {suggested_action}

Please check the dashboard for more details."""

        return await self.send_alert(message, level="WARNING")

    async def test_connection(self) -> bool:
        """Test Telegram bot connection"""
        try:
            logger.info("Testing Telegram bot connection...")

            # Get bot info
            bot_info = await self.bot.get_me()
            logger.success(f"✅ Connected to Telegram bot: @{bot_info.username}")

            # Try to send test message
            test_message = "🤖 Telegram bot connection test successful!"
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=test_message
            )

            logger.success("✅ Test message sent successfully")
            return True

        except TelegramError as e:
            logger.error(f"❌ Telegram connection test failed: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error testing Telegram: {e}")
            return False

    def disable(self):
        """Disable Telegram notifications"""
        self.enabled = False
        logger.info("🔕 Telegram notifications disabled")

    def enable(self):
        """Enable Telegram notifications"""
        self.enabled = True
        logger.info("🔔 Telegram notifications enabled")


# Global instance
telegram_bot = TelegramBot()
