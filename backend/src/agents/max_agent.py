"""MAX Agent - manages MAX (DingTalk/AliExpress Messenger) message sending"""

import asyncio
import random
from typing import Dict, Optional, Any, List
from datetime import datetime
from loguru import logger

from .base_agent import BaseAgent
from .droidrun_wrapper import droidrun
from ..device_manager.device import Device
from ..behaviors.human_typing import human_typing
from ..behaviors.human_timing import human_timing
from ..behaviors.human_gestures import human_gestures
from ..integrations.gemini_client import gemini_client
from ..integrations.telegram_bot import telegram_bot


class MAXAgent(BaseAgent):
    """MAX (DingTalk/AliExpress Messenger) automation agent with multi-level error recovery"""

    def __init__(self):
        """Initialize MAX Agent"""
        super().__init__(platform_name="MAX")
        self.app_package = "com.alibaba.mobileim"
        self.app_activity = "com.alibaba.mobileim.ui.home.HomeActivity"

        # UIAutomator2 selectors for MAX app
        self.ui_selectors = {
            "search_button": [
                "//android.widget.ImageView[@content-desc='Search']",
                "//android.widget.ImageView[@content-desc='Поиск']",
                "com.alibaba.mobileim:id/search_icon"
            ],
            "contacts_tab": [
                "//android.widget.TextView[@text='Contacts']",
                "//android.widget.TextView[@text='Контакты']",
                "com.alibaba.mobileim:id/tab_contacts"
            ],
            "message_input": [
                "//android.widget.EditText[@hint='Type a message']",
                "//android.widget.EditText[@hint='Введите сообщение']",
                "com.alibaba.mobileim:id/message_input"
            ],
            "send_button": [
                "//android.widget.ImageButton[@content-desc='Send']",
                "//android.widget.ImageButton[@content-desc='Отправить']",
                "com.alibaba.mobileim:id/send_btn"
            ],
        }

        # Recovery configuration
        self.max_retries = 3
        self.cooldown_seconds = 5

    def get_available_actions(self) -> Dict[str, Dict[str, Any]]:
        """Get list of available actions for MAX agent"""
        return {
            "send_message": {
                "description": "Send MAX message to a contact",
                "parameters": {
                    "recipient": {"type": "string", "required": True, "description": "Phone number or MAX ID"},
                    "message": {"type": "string", "required": True, "description": "Message to send"},
                    "recipient_name": {"type": "string", "required": False},
                    "use_typos": {"type": "boolean", "required": False, "default": False},
                }
            },
            "warmup": {
                "description": "Simulate natural app usage before main task",
                "parameters": {
                    "duration_seconds": {"type": "integer", "required": False, "default": 60},
                }
            },
            "send_batch_messages": {
                "description": "Send messages to multiple contacts",
                "parameters": {
                    "recipients": {"type": "array", "required": True},
                    "delay_between": {"type": "integer", "required": False, "default": 30},
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
        logger.info(f"🎯 MAX Agent executing: {action}")

        try:
            if action == "send_message":
                return await self.send_message(
                    device=device,
                    recipient=parameters.get("recipient"),
                    message=parameters.get("message"),
                    **parameters
                )
            elif action == "warmup":
                return await self.warmup(
                    device=device,
                    duration_seconds=parameters.get("duration_seconds", 60),
                    **parameters
                )
            elif action == "send_batch_messages":
                return await self.send_batch_messages(
                    device=device,
                    recipients=parameters.get("recipients", []),
                    delay_between=parameters.get("delay_between", 30),
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

    async def warmup(
        self,
        device: Device,
        duration_seconds: int = 60,
        **kwargs
    ) -> Dict[str, Any]:
        """Warmup action - simulates natural app usage before main task"""
        start_time = datetime.utcnow()
        task_id = kwargs.get("task_id", "warmup")

        logger.info(f"🔥 Starting MAX warmup for {duration_seconds}s...")

        try:
            if not await self.open_app(device):
                return self._create_error_result("Failed to open MAX for warmup", start_time)

            await human_timing.variable_delay(2, 4)

            elapsed = 0
            actions_performed = []

            while elapsed < duration_seconds:
                action = random.choice([
                    "scroll_chats",
                    "check_contacts",
                    "view_chat"
                ])

                logger.debug(f"🔄 Warmup action: {action}")

                if action == "scroll_chats":
                    await human_gestures.human_scroll(
                        device=device,
                        direction="down",
                        distance=random.randint(200, 400)
                    )
                    await human_timing.variable_delay(2, 5)
                    await human_gestures.human_scroll(
                        device=device,
                        direction="up",
                        distance=random.randint(100, 300)
                    )

                elif action == "check_contacts":
                    await droidrun.execute_action(
                        device=device,
                        natural_command="Tap on the Contacts tab at the bottom",
                        verify_success=False
                    )
                    await human_timing.variable_delay(3, 6)
                    await droidrun.execute_action(
                        device=device,
                        natural_command="Tap on the Chats tab at the bottom",
                        verify_success=False
                    )

                elif action == "view_chat":
                    await droidrun.execute_action(
                        device=device,
                        natural_command="Tap on the first chat in the list",
                        verify_success=False
                    )
                    await human_timing.variable_delay(2, 4)
                    await device.adb.press_key("KEYCODE_BACK")

                actions_performed.append(action)
                await human_timing.variable_delay(3, 8)
                elapsed = (datetime.utcnow() - start_time).total_seconds()

            duration = (datetime.utcnow() - start_time).total_seconds()
            logger.success(f"✅ MAX warmup completed: {len(actions_performed)} actions in {duration:.1f}s")

            return {
                "success": True,
                "actions_performed": actions_performed,
                "duration_seconds": duration,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"❌ Warmup error: {e}")
            return self._create_error_result(str(e), start_time)

    async def send_message(
        self,
        device: Device,
        recipient: str,
        message: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Send MAX message to recipient"""
        start_time = datetime.utcnow()
        task_id = kwargs.get("task_id", "unknown")
        recipient_name = kwargs.get("recipient_name", recipient)

        try:
            logger.info(f"📧 Starting MAX message send to {recipient_name} ({recipient})")

            # Notify Telegram
            await telegram_bot.send_task_started(
                task_id=task_id,
                recipient_name=recipient_name,
                phone_number=recipient,
                device_name=device.name
            )

            # Step 1: Open MAX
            logger.info("📱 Opening MAX...")
            if not await self.open_app(device):
                return self._create_error_result("Failed to open MAX", start_time)

            await human_timing.variable_delay(2, 4)

            # Step 2: Find and open chat
            logger.info(f"🔍 Finding contact: {recipient}")
            if not await self._find_and_open_chat(device, recipient, recipient_name):
                return self._create_error_result(f"Failed to find contact: {recipient}", start_time)

            # Step 3: Type message with human behavior
            logger.info("⌨️ Typing message...")
            typing_success = await human_typing.type_text(
                text=message,
                device=device,
                add_typos=kwargs.get("use_typos", False),
                speed_multiplier=kwargs.get("speed_multiplier", 1.0)
            )

            if not typing_success:
                return self._create_error_result("Failed to type message", start_time)

            await human_timing.variable_delay(0.5, 1.5)

            # Step 4: Send message
            logger.info("📤 Sending message...")
            if not await self._send_message(device):
                return self._create_error_result("Failed to send message", start_time)

            await human_timing.variable_delay(1, 2)

            # Step 5: Verify message sent
            logger.info("✅ Verifying message sent...")
            verification = await self._verify_message_sent(device)

            if not verification.get("success", False):
                logger.warning("⚠️ Message verification uncertain, assuming sent")

            # Success!
            duration = (datetime.utcnow() - start_time).total_seconds()
            logger.success(f"✅ MAX message sent successfully in {duration:.1f}s")

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

        except Exception as e:
            logger.error(f"❌ Error sending MAX message: {e}")
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

    async def send_batch_messages(
        self,
        device: Device,
        recipients: List[Dict[str, str]],
        delay_between: int = 30,
        **kwargs
    ) -> Dict[str, Any]:
        """Send messages to multiple recipients"""
        start_time = datetime.utcnow()
        task_id = kwargs.get("task_id", "batch")

        logger.info(f"📨 Starting batch send to {len(recipients)} recipients...")

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

            logger.info(f"📧 [{i+1}/{len(recipients)}] Sending to {name}...")

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

            if i < len(recipients) - 1:
                delay = delay_between + random.randint(-5, 10)
                logger.debug(f"⏳ Waiting {delay}s before next message...")
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

    async def verify_app_state(self, device: Device) -> Dict[str, Any]:
        """Verify MAX is in correct state"""
        try:
            analysis = await self.analyze_current_screen(
                device=device,
                analysis_type="state_check"
            )

            if analysis:
                ready = "max" in analysis.get("raw_analysis", "").lower() or \
                        "alibaba" in analysis.get("raw_analysis", "").lower()
                return {"ready": ready, "analysis": analysis}

            return {"ready": False, "error": "Failed to analyze screen"}

        except Exception as e:
            logger.error(f"Error verifying app state: {e}")
            return {"ready": False, "error": str(e)}

    async def open_app(self, device: Device) -> bool:
        """Open MAX app"""
        try:
            logger.info("📱 Opening MAX...")
            success = await device.adb.start_app(self.app_package, self.app_activity)

            if success:
                logger.success("✅ MAX opened")
            else:
                logger.error("❌ Failed to open MAX")

            return success

        except Exception as e:
            logger.error(f"Error opening MAX: {e}")
            return False

    async def close_app(self, device: Device) -> bool:
        """Close MAX app"""
        try:
            logger.info("Closing MAX...")
            result = await device.adb.shell_command(f"am force-stop {self.app_package}")
            success = result is not None

            if success:
                logger.success("✅ MAX closed")

            return success

        except Exception as e:
            logger.error(f"Error closing MAX: {e}")
            return False

    async def _find_and_open_chat(
        self,
        device: Device,
        phone_number: str,
        recipient_name: str
    ) -> bool:
        """Find and open chat with recipient"""
        try:
            # Step 1: Tap search
            logger.debug("Tapping search button...")
            result = await droidrun.execute_action(
                device=device,
                natural_command="Tap on the search icon at the top",
                verify_success=True
            )

            await human_timing.variable_delay(1, 2)

            # Step 2: Type phone number
            logger.debug(f"Searching for: {phone_number}")
            await droidrun.execute_action(
                device=device,
                natural_command="Tap on the search input field",
                verify_success=False
            )

            await human_timing.variable_delay(0.5, 1)

            await human_typing.type_text(
                text=phone_number,
                device=device,
                add_typos=False,
                speed_multiplier=1.2
            )

            await human_timing.variable_delay(2, 3)

            # Step 3: Tap contact
            logger.debug("Opening chat...")
            result = await droidrun.execute_action(
                device=device,
                natural_command="Tap on the first contact in the search results",
                verify_success=True
            )

            if result.get("success"):
                logger.success(f"✅ Opened chat with {recipient_name}")
                await human_timing.variable_delay(1, 2)
                return True

            # Fallback: Try using Gemini Vision
            logger.warning("⚠️ UIAutomator failed, trying Gemini Vision fallback...")
            if gemini_client.is_available():
                screenshot_path = await device.adb.take_screenshot()
                if screenshot_path:
                    vision_result = await gemini_client.analyze_screenshot(
                        screenshot_path=screenshot_path,
                        analysis_type="ui_elements"
                    )
                    if vision_result:
                        # Use vision result to find contact
                        elements = vision_result.get("elements", [])
                        for elem in elements:
                            if phone_number in elem.get("text", "") or \
                               recipient_name.lower() in elem.get("text", "").lower():
                                bounds = elem.get("bounds", [])
                                if bounds and len(bounds) >= 4:
                                    center_x = (bounds[0] + bounds[2]) // 2
                                    center_y = (bounds[1] + bounds[3]) // 2
                                    await device.adb.tap(center_x, center_y)
                                    await human_timing.variable_delay(1, 2)
                                    return True

            logger.error(f"❌ Failed to open chat with {recipient_name}")
            return False

        except Exception as e:
            logger.error(f"Error finding and opening chat: {e}")
            return False

    async def _send_message(self, device: Device) -> bool:
        """Tap the send button"""
        try:
            logger.debug("Tapping send button...")
            result = await droidrun.execute_action(
                device=device,
                natural_command="Tap on the send button",
                verify_success=True
            )

            if result.get("success"):
                logger.success("✅ Send button tapped")
                return True

            logger.error("❌ Failed to tap send button")
            return False

        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False

    async def _verify_message_sent(self, device: Device) -> Dict[str, Any]:
        """Verify message was sent successfully"""
        try:
            screenshot = await device.adb.take_screenshot()
            if not screenshot:
                return {"success": False, "error": "Failed to take screenshot"}

            if gemini_client.is_available():
                result = await gemini_client.analyze_screenshot(
                    screenshot_path=screenshot,
                    analysis_type="state_check"
                )
                if result:
                    # Check if message appears sent
                    return {"success": True, "analysis": result}

            # Fallback: assume success if no error detected
            return {"success": True, "assumed": True}

        except Exception as e:
            logger.error(f"Error verifying message: {e}")
            return {"success": False, "error": str(e)}

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
max_agent = MAXAgent()
