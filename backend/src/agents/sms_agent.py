"""SMS Agent - manages native Android SMS sending"""

import asyncio
import random
from typing import Dict, Optional, Any, List
from datetime import datetime
from loguru import logger

from .base_agent import BaseAgent
from ..device_manager.device import Device
from ..behaviors.human_typing import human_typing
from ..behaviors.human_timing import human_timing
from ..integrations.gemini_client import gemini_client
from ..integrations.telegram_bot import telegram_bot


def validate_phone_number(phone: str) -> bool:
    """Validate international phone number format"""
    cleaned = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if cleaned.startswith("+"):
        cleaned = cleaned[1:]
    if not cleaned.isdigit():
        return False
    if len(cleaned) < 7 or len(cleaned) > 15:
        return False
    return True


class SMSAgent(BaseAgent):
    """Native Android SMS automation agent"""

    def __init__(self):
        """Initialize SMS Agent"""
        super().__init__(platform_name="SMS")
        self.app_package = "com.google.android.apps.messaging"
        self.app_activity = "com.google.android.apps.messaging.ui.ConversationListActivity"

        # Alternative SMS app packages (for different devices)
        self.alternative_packages = [
            ("com.android.mms", "com.android.mms.ui.ConversationList"),
            ("com.samsung.android.messaging", "com.samsung.android.messaging.ui.view.main.MainActivity"),
        ]

        # Max SMS length (before splitting)
        self.max_sms_length = 160
        self.max_concat_sms = 3  # Max 3 parts = 480 chars

    def get_available_actions(self) -> Dict[str, Dict[str, Any]]:
        """Get list of available actions for SMS agent"""
        return {
            "send_message": {
                "description": "Send SMS message to a phone number",
                "parameters": {
                    "recipient": {"type": "string", "required": True, "description": "Phone number with country code"},
                    "message": {"type": "string", "required": True, "description": "Message to send (max 480 chars)"},
                    "recipient_name": {"type": "string", "required": False},
                }
            },
            "send_batch_messages": {
                "description": "Send SMS messages to multiple recipients",
                "parameters": {
                    "recipients": {"type": "array", "required": True},
                    "delay_between": {"type": "integer", "required": False, "default": 60},
                }
            },
            "check_delivery": {
                "description": "Check SMS delivery status",
                "parameters": {
                    "recipient": {"type": "string", "required": True},
                }
            }
        }

    async def execute(
        self,
        device: Device,
        action: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute an action"""
        logger.info(f"🎯 SMS Agent executing: {action}")

        try:
            if action == "send_message":
                return await self.send_message(
                    device=device,
                    recipient=parameters.get("recipient"),
                    message=parameters.get("message"),
                    **parameters
                )
            elif action == "send_batch_messages":
                return await self.send_batch_messages(
                    device=device,
                    recipients=parameters.get("recipients", []),
                    delay_between=parameters.get("delay_between", 60),
                    **parameters
                )
            elif action == "check_delivery":
                return await self.check_delivery_status(
                    device=device,
                    recipient=parameters.get("recipient"),
                    **parameters
                )
            else:
                return {
                    "success": False,
                    "error": f"Unknown action: {action}",
                    "available_actions": list(self.get_available_actions().keys())
                }
        except Exception as e:
            logger.error(f"❌ Action execution error: {e}")
            return {"success": False, "error": str(e)}

    async def send_message(
        self,
        device: Device,
        recipient: str,
        message: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Send SMS message to recipient using ADB"""
        start_time = datetime.utcnow()
        task_id = kwargs.get("task_id", "unknown")
        recipient_name = kwargs.get("recipient_name", recipient)

        try:
            logger.info(f"📱 Starting SMS send to {recipient_name} ({recipient})")

            # Validate phone number
            if not validate_phone_number(recipient):
                error_msg = f"Invalid phone number format: {recipient}"
                logger.error(f"❌ {error_msg}")
                return self._create_error_result(error_msg, start_time)

            # Check message length
            if len(message) > self.max_sms_length * self.max_concat_sms:
                error_msg = f"Message too long: {len(message)} chars (max {self.max_sms_length * self.max_concat_sms})"
                logger.warning(f"⚠️ {error_msg}")
                # Truncate message
                message = message[:self.max_sms_length * self.max_concat_sms - 3] + "..."

            # Notify Telegram
            await telegram_bot.send_task_started(
                task_id=task_id,
                recipient_name=recipient_name,
                phone_number=recipient,
                device_name=device.name
            )

            # Method 1: Use ADB shell to send SMS directly (preferred)
            success = await self._send_sms_via_adb(device, recipient, message)

            if not success:
                # Method 2: Use SMS intent (fallback)
                logger.warning("⚠️ Direct SMS failed, trying intent method...")
                success = await self._send_sms_via_intent(device, recipient, message)

            if not success:
                # Method 3: Open messaging app and send manually
                logger.warning("⚠️ Intent method failed, trying app automation...")
                success = await self._send_sms_via_app(device, recipient, message)

            if success:
                duration = (datetime.utcnow() - start_time).total_seconds()
                logger.success(f"✅ SMS sent successfully in {duration:.1f}s")

                self._update_action_metrics()

                await telegram_bot.send_task_completed(
                    task_id=task_id,
                    recipient_name=recipient_name,
                    phone_number=recipient,
                    device_name=device.name,
                    duration_seconds=duration
                )

                return {
                    "success": True,
                    "recipient": recipient,
                    "message": message,
                    "duration_seconds": duration,
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                return self._create_error_result("All SMS send methods failed", start_time)

        except Exception as e:
            logger.error(f"❌ Error sending SMS: {e}")
            duration = (datetime.utcnow() - start_time).total_seconds()

            await telegram_bot.send_task_failed(
                task_id=task_id,
                recipient_name=recipient_name,
                phone_number=recipient,
                device_name=device.name,
                error_message=str(e),
                attempt_count=kwargs.get("attempt_count", 1)
            )

            return self._create_error_result(str(e), start_time)

    async def _send_sms_via_adb(self, device: Device, recipient: str, message: str) -> bool:
        """Send SMS using ADB shell command (requires root or special permissions)"""
        try:
            # Escape special characters in message
            escaped_message = message.replace('"', '\\"').replace("'", "\\'")

            # Try using service call (works on some devices)
            cmd = f'service call isms 7 i32 0 s16 "com.android.mms" s16 "{recipient}" s16 "null" s16 "{escaped_message}" s16 "null" s16 "null"'
            result = await device.adb.shell_command(cmd)

            if result and "Result: Parcel" in result:
                logger.success("✅ SMS sent via service call")
                return True

            return False

        except Exception as e:
            logger.debug(f"ADB SMS method failed: {e}")
            return False

    async def _send_sms_via_intent(self, device: Device, recipient: str, message: str) -> bool:
        """Send SMS using Android intent"""
        try:
            # Escape special characters
            escaped_message = message.replace('"', '\\"').replace("'", "\\'").replace(" ", "%20")

            # Use am start with SMS intent
            cmd = f'am start -a android.intent.action.SENDTO -d "sms:{recipient}" --es sms_body "{escaped_message}" --ez exit_on_sent true'
            result = await device.adb.shell_command(cmd)

            if result:
                # Wait for messaging app to open
                await asyncio.sleep(2)

                # Tap send button
                await device.adb.input_keyevent("KEYCODE_ENTER")
                await asyncio.sleep(1)

                logger.success("✅ SMS sent via intent")
                return True

            return False

        except Exception as e:
            logger.debug(f"Intent SMS method failed: {e}")
            return False

    async def _send_sms_via_app(self, device: Device, recipient: str, message: str) -> bool:
        """Send SMS by automating the messaging app"""
        try:
            # Open messaging app
            if not await self.open_app(device):
                return False

            await human_timing.variable_delay(2, 3)

            # Start new conversation
            from .droidrun_wrapper import droidrun

            result = await droidrun.execute_action(
                device=device,
                natural_command="Tap on the new message or compose button",
                verify_success=False
            )

            await human_timing.variable_delay(1, 2)

            # Enter recipient
            await human_typing.type_text(
                text=recipient,
                device=device,
                add_typos=False,
                speed_multiplier=1.0
            )

            await device.adb.input_keyevent("KEYCODE_ENTER")
            await human_timing.variable_delay(1, 2)

            # Enter message
            result = await droidrun.execute_action(
                device=device,
                natural_command="Tap on the message input field",
                verify_success=False
            )

            await human_timing.variable_delay(0.5, 1)

            await human_typing.type_text(
                text=message,
                device=device,
                add_typos=False,
                speed_multiplier=0.9
            )

            await human_timing.variable_delay(0.5, 1)

            # Tap send
            result = await droidrun.execute_action(
                device=device,
                natural_command="Tap on the send button",
                verify_success=True
            )

            if result.get("success"):
                logger.success("✅ SMS sent via app automation")
                return True

            return False

        except Exception as e:
            logger.error(f"App SMS method failed: {e}")
            return False

    async def send_batch_messages(
        self,
        device: Device,
        recipients: List[Dict[str, str]],
        delay_between: int = 60,
        **kwargs
    ) -> Dict[str, Any]:
        """Send SMS to multiple recipients"""
        start_time = datetime.utcnow()
        task_id = kwargs.get("task_id", "batch")

        logger.info(f"📨 Starting SMS batch send to {len(recipients)} recipients...")

        results = []
        success_count = 0
        failure_count = 0

        for i, recipient in enumerate(recipients):
            phone = recipient.get("phone")
            name = recipient.get("name", phone)
            message = recipient.get("message")

            if not phone or not message:
                results.append({
                    "phone": phone,
                    "success": False,
                    "error": "Missing phone or message"
                })
                failure_count += 1
                continue

            logger.info(f"📧 [{i+1}/{len(recipients)}] Sending SMS to {name}...")

            result = await self.send_message(
                device=device,
                recipient=phone,
                message=message,
                recipient_name=name,
                task_id=f"{task_id}_{i}",
                **kwargs
            )

            results.append({
                "phone": phone,
                "name": name,
                "success": result.get("success", False),
                "error": result.get("error"),
                "duration": result.get("duration_seconds")
            })

            if result.get("success"):
                success_count += 1
            else:
                failure_count += 1

            # SMS has stricter rate limits - longer delay
            if i < len(recipients) - 1:
                delay = delay_between + random.randint(-10, 20)
                logger.debug(f"⏳ Waiting {delay}s before next SMS...")
                await asyncio.sleep(delay)

        duration = (datetime.utcnow() - start_time).total_seconds()

        return {
            "success": failure_count == 0,
            "total": len(recipients),
            "success_count": success_count,
            "failure_count": failure_count,
            "results": results,
            "duration_seconds": duration,
            "timestamp": datetime.utcnow().isoformat()
        }

    async def check_delivery_status(
        self,
        device: Device,
        recipient: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Check SMS delivery status"""
        try:
            # Open messaging app and find conversation
            if not await self.open_app(device):
                return {"success": False, "error": "Failed to open messaging app"}

            await human_timing.variable_delay(2, 3)

            # Search for conversation
            from .droidrun_wrapper import droidrun

            result = await droidrun.execute_action(
                device=device,
                natural_command=f"Find and open conversation with {recipient}",
                verify_success=False
            )

            await human_timing.variable_delay(1, 2)

            # Take screenshot and analyze
            if gemini_client.is_available():
                screenshot = await device.adb.take_screenshot()
                if screenshot:
                    analysis = await gemini_client.analyze_screenshot(
                        screenshot_path=screenshot,
                        analysis_type="state_check"
                    )

                    if analysis:
                        return {
                            "success": True,
                            "status": "analyzed",
                            "analysis": analysis
                        }

            return {
                "success": True,
                "status": "unknown",
                "message": "Could not determine delivery status"
            }

        except Exception as e:
            logger.error(f"Error checking delivery: {e}")
            return {"success": False, "error": str(e)}

    async def verify_app_state(self, device: Device) -> Dict[str, Any]:
        """Verify messaging app is in correct state"""
        try:
            analysis = await self.analyze_current_screen(
                device=device,
                analysis_type="state_check"
            )

            if analysis:
                raw = analysis.get("raw_analysis", "").lower()
                ready = "message" in raw or "sms" in raw or "chat" in raw
                return {"ready": ready, "analysis": analysis}

            return {"ready": False, "error": "Failed to analyze screen"}

        except Exception as e:
            logger.error(f"Error verifying app state: {e}")
            return {"ready": False, "error": str(e)}

    async def open_app(self, device: Device) -> bool:
        """Open messaging app"""
        try:
            logger.info("📱 Opening Messages app...")

            # Try primary package
            success = await device.adb.start_app(self.app_package, self.app_activity)

            if not success:
                # Try alternative packages
                for alt_package, alt_activity in self.alternative_packages:
                    success = await device.adb.start_app(alt_package, alt_activity)
                    if success:
                        self.app_package = alt_package
                        self.app_activity = alt_activity
                        break

            if success:
                logger.success("✅ Messages app opened")
            else:
                logger.error("❌ Failed to open Messages app")

            return success

        except Exception as e:
            logger.error(f"Error opening Messages app: {e}")
            return False

    async def close_app(self, device: Device) -> bool:
        """Close messaging app"""
        try:
            logger.info("Closing Messages app...")
            result = await device.adb.shell_command(f"am force-stop {self.app_package}")
            success = result is not None

            if success:
                logger.success("✅ Messages app closed")

            return success

        except Exception as e:
            logger.error(f"Error closing Messages app: {e}")
            return False

    def _create_error_result(self, error_message: str, start_time: datetime) -> Dict[str, Any]:
        """Create standardized error result"""
        duration = (datetime.utcnow() - start_time).total_seconds()
        return {
            "success": False,
            "error": error_message,
            "duration_seconds": duration,
            "timestamp": datetime.utcnow().isoformat()
        }


# Global instance
sms_agent = SMSAgent()
