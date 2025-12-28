"""WhatsApp Agent - manages WhatsApp message sending"""

import asyncio
import re
import random
from typing import Dict, Optional, Any, List, Callable
from datetime import datetime
from enum import Enum, auto
from loguru import logger

from .base_agent import BaseAgent
from .droidrun_wrapper import droidrun
from ..device_manager.device import Device
from ..behaviors.human_typing import human_typing
from ..behaviors.human_timing import human_timing
from ..behaviors.human_gestures import human_gestures
from ..integrations.puter_client import puter_client
from ..integrations.telegram_bot import telegram_bot


class RecoveryLevel(Enum):
    """Error recovery levels - escalating recovery strategies"""
    RETRY_ACTION = 1      # Just retry the failed action
    RESTART_STEP = 2      # Restart the current step from beginning
    RESTART_APP = 3       # Force close and restart WhatsApp
    RESTART_DEVICE = 4    # Soft restart Android shell
    HARD_RESTART = 5      # Full device reboot (last resort)


class ActionResult(Enum):
    """Result of an action attempt"""
    SUCCESS = auto()
    RETRY = auto()          # Should retry same action
    ESCALATE = auto()       # Should escalate recovery level
    ABORT = auto()          # Should abort entirely


# Error patterns and their recommended recovery levels
ERROR_RECOVERY_MAP = {
    # App-level errors
    "app not responding": RecoveryLevel.RESTART_APP,
    "app crashed": RecoveryLevel.RESTART_APP,
    "com.whatsapp has stopped": RecoveryLevel.RESTART_APP,
    "unfortunately": RecoveryLevel.RESTART_APP,

    # UI errors
    "element not found": RecoveryLevel.RETRY_ACTION,
    "tap failed": RecoveryLevel.RETRY_ACTION,
    "timeout": RecoveryLevel.RESTART_STEP,
    "screen changed unexpectedly": RecoveryLevel.RESTART_STEP,

    # Connection errors
    "no internet": RecoveryLevel.RESTART_DEVICE,
    "connection failed": RecoveryLevel.RESTART_STEP,
    "server unreachable": RecoveryLevel.RESTART_STEP,

    # Device errors
    "device offline": RecoveryLevel.HARD_RESTART,
    "adb disconnected": RecoveryLevel.RESTART_DEVICE,
    "shell not responding": RecoveryLevel.RESTART_DEVICE,
}


def validate_phone_number(phone: str) -> bool:
    """
    Validate international phone number format

    Args:
        phone: Phone number to validate

    Returns:
        bool: True if valid, False otherwise

    Valid formats:
        +66812345678 (with country code)
        66812345678 (without + prefix)
        +1-555-123-4567 (with dashes)
        +44 20 1234 5678 (with spaces)
    """
    # Remove spaces and dashes
    cleaned = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

    # Check if it starts with + or just digits
    if cleaned.startswith("+"):
        cleaned = cleaned[1:]

    # Must be 7-15 digits (international standard)
    if not cleaned.isdigit():
        return False

    if len(cleaned) < 7 or len(cleaned) > 15:
        return False

    return True


class WhatsAppAgent(BaseAgent):
    """WhatsApp automation agent with multi-level error recovery"""

    def __init__(self):
        """Initialize WhatsApp Agent"""
        super().__init__(platform_name="WhatsApp")
        self.app_package = "com.whatsapp"
        self.app_activity = "com.whatsapp.HomeActivity"

        # Recovery configuration
        self.max_retries_per_level = {
            RecoveryLevel.RETRY_ACTION: 3,
            RecoveryLevel.RESTART_STEP: 2,
            RecoveryLevel.RESTART_APP: 2,
            RecoveryLevel.RESTART_DEVICE: 1,
            RecoveryLevel.HARD_RESTART: 1,
        }

        # Cooldown between recovery attempts (seconds)
        self.recovery_cooldowns = {
            RecoveryLevel.RETRY_ACTION: 1,
            RecoveryLevel.RESTART_STEP: 3,
            RecoveryLevel.RESTART_APP: 5,
            RecoveryLevel.RESTART_DEVICE: 15,
            RecoveryLevel.HARD_RESTART: 60,
        }

        # UIAutomator2 fallback selectors (for direct element interaction)
        self.ui_selectors = {
            "search_button": ["//android.widget.ImageView[@content-desc='Search']",
                              "//android.widget.ImageView[@content-desc='Поиск']",
                              "com.whatsapp:id/menuitem_search"],
            "new_chat_fab": ["//android.widget.ImageButton[@content-desc='New chat']",
                             "//android.widget.ImageButton[@content-desc='Новый чат']",
                             "com.whatsapp:id/fab"],
            "search_input": ["//android.widget.EditText[@text='Search...']",
                             "//android.widget.EditText[@text='Поиск...']",
                             "com.whatsapp:id/search_src_text"],
            "message_input": ["//android.widget.EditText[@text='Type a message']",
                              "//android.widget.EditText[@text='Введите сообщение']",
                              "com.whatsapp:id/entry"],
            "send_button": ["//android.widget.ImageButton[@content-desc='Send']",
                            "//android.widget.ImageButton[@content-desc='Отправить']",
                            "com.whatsapp:id/send"],
        }

    def _determine_recovery_level(self, error: str) -> RecoveryLevel:
        """
        Determine appropriate recovery level based on error

        Args:
            error: Error message

        Returns:
            RecoveryLevel: Recommended recovery level
        """
        error_lower = error.lower()

        for pattern, level in ERROR_RECOVERY_MAP.items():
            if pattern in error_lower:
                return level

        # Default to retry action for unknown errors
        return RecoveryLevel.RETRY_ACTION

    async def _execute_recovery(
        self,
        device: Device,
        level: RecoveryLevel
    ) -> bool:
        """
        Execute recovery action at specified level

        Args:
            device: Device instance
            level: Recovery level

        Returns:
            bool: True if recovery succeeded
        """
        logger.info(f"🔄 Executing recovery at level: {level.name}")

        cooldown = self.recovery_cooldowns.get(level, 2)
        await asyncio.sleep(cooldown)

        try:
            if level == RecoveryLevel.RETRY_ACTION:
                # Just wait and retry - no special action
                await human_timing.variable_delay(1, 2)
                return True

            elif level == RecoveryLevel.RESTART_STEP:
                # Clear any popups/dialogs and return to main screen
                await device.adb.press_key("KEYCODE_BACK")
                await asyncio.sleep(0.5)
                await device.adb.press_key("KEYCODE_BACK")
                await asyncio.sleep(1)
                return True

            elif level == RecoveryLevel.RESTART_APP:
                # Force stop and restart WhatsApp
                await device.adb.shell_command(f"am force-stop {self.app_package}")
                await asyncio.sleep(2)
                success = await self.open_app(device)
                await asyncio.sleep(3)
                return success

            elif level == RecoveryLevel.RESTART_DEVICE:
                # Soft restart Android shell (stops and restarts zygote)
                logger.warning("⚠️ Performing soft device restart...")
                await device.adb.shell_command("stop")
                await asyncio.sleep(2)
                await device.adb.shell_command("start")
                await asyncio.sleep(10)
                return True

            elif level == RecoveryLevel.HARD_RESTART:
                # Full device reboot
                logger.warning("⚠️ Performing full device reboot...")
                await device.adb.shell_command("reboot")
                # Wait for device to come back online
                for _ in range(30):  # Wait up to 60 seconds
                    await asyncio.sleep(2)
                    if await device.check_connection():
                        await asyncio.sleep(10)  # Additional wait after boot
                        return True
                return False

            return False

        except Exception as e:
            logger.error(f"Recovery failed at level {level.name}: {e}")
            return False

    async def _execute_with_recovery(
        self,
        device: Device,
        action: Callable,
        action_name: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute action with multi-level recovery

        Args:
            device: Device instance
            action: Async action function to execute
            action_name: Name for logging
            **kwargs: Arguments for action

        Returns:
            dict: Result with success status
        """
        current_level = RecoveryLevel.RETRY_ACTION
        level_attempts = {level: 0 for level in RecoveryLevel}

        while True:
            try:
                logger.debug(f"Executing action: {action_name}")
                result = await action(**kwargs)

                if result.get("success", False):
                    return result

                # Action failed - determine recovery level
                error = result.get("error", "unknown error")
                recommended_level = self._determine_recovery_level(error)

                # Use higher of current and recommended level
                if recommended_level.value > current_level.value:
                    current_level = recommended_level

            except Exception as e:
                error = str(e)
                current_level = self._determine_recovery_level(error)

            # Check if we've exceeded retries at current level
            level_attempts[current_level] += 1
            max_retries = self.max_retries_per_level.get(current_level, 1)

            if level_attempts[current_level] > max_retries:
                # Escalate to next level
                if current_level.value < RecoveryLevel.HARD_RESTART.value:
                    current_level = RecoveryLevel(current_level.value + 1)
                    logger.warning(f"⬆️ Escalating recovery to: {current_level.name}")
                else:
                    # All recovery levels exhausted
                    logger.error(f"❌ All recovery attempts failed for: {action_name}")
                    return {"success": False, "error": f"All recovery attempts exhausted: {error}"}

            # Execute recovery
            recovery_success = await self._execute_recovery(device, current_level)
            if not recovery_success:
                logger.warning(f"Recovery at level {current_level.name} failed, trying next level")
                continue

    async def warmup(
        self,
        device: Device,
        duration_seconds: int = 60,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Warmup action - simulates natural app usage before main task

        Args:
            device: Device instance
            duration_seconds: Warmup duration
            **kwargs: Optional parameters

        Returns:
            dict: Result with warmup status
        """
        start_time = datetime.utcnow()
        task_id = kwargs.get("task_id", "warmup")

        logger.info(f"🔥 Starting WhatsApp warmup for {duration_seconds}s...")

        try:
            # Open WhatsApp
            if not await self.open_app(device):
                return self._create_error_result("Failed to open WhatsApp for warmup", start_time)

            await human_timing.variable_delay(2, 4)

            elapsed = 0
            actions_performed = []

            while elapsed < duration_seconds:
                # Choose random warmup action
                action = random.choice([
                    "scroll_chats",
                    "view_status",
                    "open_random_chat",
                    "check_settings"
                ])

                logger.debug(f"🔄 Warmup action: {action}")

                if action == "scroll_chats":
                    # Scroll through chat list
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

                elif action == "view_status":
                    # Tap on Status tab
                    await droidrun.execute_action(
                        device=device,
                        natural_command="Tap on the Status tab at the bottom",
                        verify_success=False
                    )
                    await human_timing.variable_delay(3, 6)

                    # Return to Chats
                    await droidrun.execute_action(
                        device=device,
                        natural_command="Tap on the Chats tab at the bottom",
                        verify_success=False
                    )

                elif action == "open_random_chat":
                    # Open a recent chat and close it
                    await droidrun.execute_action(
                        device=device,
                        natural_command="Tap on the first chat in the list",
                        verify_success=False
                    )
                    await human_timing.variable_delay(2, 4)

                    # Go back without sending anything
                    await device.adb.press_key("KEYCODE_BACK")

                elif action == "check_settings":
                    # Open settings briefly
                    await droidrun.execute_action(
                        device=device,
                        natural_command="Tap on the three dots menu button",
                        verify_success=False
                    )
                    await human_timing.variable_delay(1, 2)

                    # Close menu
                    await device.adb.press_key("KEYCODE_BACK")

                actions_performed.append(action)
                await human_timing.variable_delay(3, 8)

                elapsed = (datetime.utcnow() - start_time).total_seconds()

            duration = (datetime.utcnow() - start_time).total_seconds()
            logger.success(f"✅ Warmup completed: {len(actions_performed)} actions in {duration:.1f}s")

            return {
                "success": True,
                "actions_performed": actions_performed,
                "duration_seconds": duration,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"❌ Warmup error: {e}")
            return self._create_error_result(str(e), start_time)

    async def _tap_element_uiautomator(
        self,
        device: Device,
        element_key: str
    ) -> bool:
        """
        Tap element using UIAutomator2 selectors (fallback)

        Args:
            device: Device instance
            element_key: Key from ui_selectors

        Returns:
            bool: True if successful
        """
        selectors = self.ui_selectors.get(element_key, [])

        for selector in selectors:
            try:
                # Try to find and tap element using uiautomator
                if selector.startswith("//"):
                    # XPath selector
                    cmd = f"uiautomator dump /dev/tty 2>/dev/null | grep -o '{selector}'"
                    result = await device.adb.shell_command(cmd)
                    if result:
                        # Extract bounds and tap center
                        # This is a simplified approach
                        tap_result = await droidrun.execute_action(
                            device=device,
                            natural_command=f"Find and tap element: {element_key}",
                            verify_success=True
                        )
                        if tap_result.get("success"):
                            return True
                else:
                    # Resource ID selector
                    cmd = f"input tap $(dumpsys window windows | grep -E 'mCurrentFocus' | cut -d'/' -f1 | cut -d' ' -f3)"
                    # Simplified - in production would parse UI hierarchy
                    pass

            except Exception as e:
                logger.debug(f"Selector {selector} failed: {e}")
                continue

        return False

    def get_available_actions(self) -> Dict[str, Dict[str, Any]]:
        """
        Get list of available actions for this agent

        Returns:
            dict: Available actions with their parameters
        """
        return {
            "send_message": {
                "description": "Send WhatsApp message to a phone number",
                "parameters": {
                    "recipient": {"type": "string", "required": True, "description": "Phone number with country code"},
                    "message": {"type": "string", "required": True, "description": "Message to send"},
                    "personalize": {"type": "boolean", "required": False, "default": False},
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
                "description": "Send messages to multiple recipients",
                "parameters": {
                    "recipients": {"type": "array", "required": True, "description": "List of {phone, name, message}"},
                    "delay_between": {"type": "integer", "required": False, "default": 30},
                }
            },
            "check_delivery": {
                "description": "Check if a message was delivered",
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
        """
        Execute an action (called by ScenarioRunner)

        Args:
            device: Device instance
            action: Action name (e.g., "send_message", "warmup")
            parameters: Action parameters

        Returns:
            dict: Execution result
        """
        logger.info(f"🎯 WhatsApp Agent executing: {action}")

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

    async def send_batch_messages(
        self,
        device: Device,
        recipients: List[Dict[str, str]],
        delay_between: int = 30,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send messages to multiple recipients

        Args:
            device: Device instance
            recipients: List of {"phone": str, "name": str, "message": str}
            delay_between: Delay between messages in seconds
            **kwargs: Additional options

        Returns:
            dict: Batch result with success/failure counts
        """
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

            # Send message
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

            # Delay between messages (with human variation)
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

    async def check_delivery_status(
        self,
        device: Device,
        recipient: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Check if last message to recipient was delivered

        Args:
            device: Device instance
            recipient: Phone number

        Returns:
            dict: Delivery status
        """
        try:
            # Open WhatsApp and find chat
            if not await self.open_app(device):
                return {"success": False, "error": "Failed to open WhatsApp"}

            await human_timing.variable_delay(2, 3)

            # Search for contact
            if not await self._find_and_open_chat(device, recipient, recipient):
                return {"success": False, "error": "Could not find chat"}

            # Analyze chat to check delivery status
            screenshot = await device.adb.take_screenshot()

            prompt = """Analyze this WhatsApp chat screenshot.
Look at the last message sent by the user (outgoing message, usually on the right side).
Check its delivery status:
- Single gray checkmark = Sent
- Double gray checkmarks = Delivered
- Double blue checkmarks = Read
- Clock icon = Pending/Not sent

Return JSON:
{
  "success": true,
  "status": "sent" | "delivered" | "read" | "pending" | "failed",
  "timestamp": "approximate time if visible",
  "confidence": 0-100
}"""

            response = await puter_client._generate(prompt=prompt, model="claude-sonnet-4.5")

            if response and "{" in response:
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                result = json.loads(response[start:end])
                return result

            return {"success": False, "error": "Could not analyze delivery status"}

        except Exception as e:
            logger.error(f"Error checking delivery: {e}")
            return {"success": False, "error": str(e)}

    async def send_message(
        self,
        device: Device,
        recipient: str,
        message: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send WhatsApp message to recipient

        Args:
            device: Device instance to use
            recipient: Phone number (e.g., "+66812345678")
            message: Message content
            **kwargs: Optional parameters:
                - personalize (bool): Use LLM to personalize message
                - recipient_name (str): Recipient name for personalization
                - context (str): Additional context for personalization
                - use_typos (bool): Add realistic typos
                - speed_multiplier (float): Typing speed multiplier

        Returns:
            dict: Result with success status and metadata
        """
        start_time = datetime.utcnow()
        task_id = kwargs.get("task_id", "unknown")
        recipient_name = kwargs.get("recipient_name", recipient)

        try:
            logger.info(f"📧 Starting WhatsApp message send to {recipient_name} ({recipient})")

            # Validate phone number format
            if not validate_phone_number(recipient):
                error_msg = f"Invalid phone number format: {recipient}"
                logger.error(f"❌ {error_msg}")
                return self._create_error_result(error_msg, start_time)

            # Notify Telegram
            await telegram_bot.send_task_started(
                task_id=task_id,
                recipient_name=recipient_name,
                phone_number=recipient,
                device_name=device.name
            )

            # Step 1: Personalize message if requested
            if kwargs.get("personalize", False):
                logger.info("🤖 Personalizing message with LLM...")
                personalized = await puter_client.generate_message(
                    recipient_name=recipient_name,
                    context=kwargs.get("context"),
                    template=message
                )
                if personalized:
                    message = personalized
                    logger.success("✅ Message personalized")

            # Step 2: Open WhatsApp
            logger.info("📱 Opening WhatsApp...")
            if not await self.open_app(device):
                return self._create_error_result("Failed to open WhatsApp", start_time)

            # Wait for app to load
            await human_timing.variable_delay(2, 4)

            # Step 3: Verify app state
            app_state = await self.verify_app_state(device)
            if not app_state.get("ready", False):
                logger.warning("⚠️ App not ready, attempting recovery...")
                await self.restart_app(device)
                await human_timing.variable_delay(3, 5)

            # Step 4: Navigate to new chat / search contact
            logger.info(f"🔍 Finding contact: {recipient}")
            if not await self._find_and_open_chat(device, recipient, recipient_name):
                return self._create_error_result(f"Failed to find contact: {recipient}", start_time)

            # Step 5: Type message with human behavior
            logger.info("⌨️ Typing message...")
            typing_success = await human_typing.type_text(
                text=message,
                device=device,
                add_typos=kwargs.get("use_typos", False),
                speed_multiplier=kwargs.get("speed_multiplier", 1.0)
            )

            if not typing_success:
                return self._create_error_result("Failed to type message", start_time)

            # Small delay before sending
            await human_timing.variable_delay(0.5, 1.5)

            # Step 6: Send message
            logger.info("📤 Sending message...")
            if not await self._send_message(device):
                return self._create_error_result("Failed to send message", start_time)

            # Wait for message to send
            await human_timing.variable_delay(1, 2)

            # Step 7: Verify message sent
            logger.info("✅ Verifying message sent...")
            verification = await self._verify_message_sent(device)

            if not verification.get("success", False):
                return self._create_error_result("Message may not have sent", start_time)

            # Success!
            duration = (datetime.utcnow() - start_time).total_seconds()
            logger.success(f"✅ WhatsApp message sent successfully in {duration:.1f}s")

            # Update metrics
            self._update_action_metrics()

            # Notify Telegram
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
            logger.error(f"❌ Error sending WhatsApp message: {e}")
            duration = (datetime.utcnow() - start_time).total_seconds()

            # Notify Telegram
            await telegram_bot.send_task_failed(
                task_id=task_id,
                recipient_name=recipient_name,
                phone_number=recipient,
                device_name=device.name,
                error_message=str(e),
                attempt_count=kwargs.get("attempt_count", 1)
            )

            return self._create_error_result(str(e), start_time)

    async def verify_app_state(self, device: Device) -> Dict[str, Any]:
        """
        Verify WhatsApp is in correct state

        Args:
            device: Device instance

        Returns:
            dict: App state information
        """
        try:
            # Take screenshot and analyze
            analysis = await self.analyze_current_screen(
                device=device,
                analysis_type="state_check"
            )

            if analysis:
                # Check if we're on a valid WhatsApp screen
                ready = analysis.get("raw_analysis", "").lower().find("whatsapp") >= 0
                return {"ready": ready, "analysis": analysis}

            return {"ready": False, "error": "Failed to analyze screen"}

        except Exception as e:
            logger.error(f"Error verifying app state: {e}")
            return {"ready": False, "error": str(e)}

    async def open_app(self, device: Device) -> bool:
        """
        Open WhatsApp app

        Args:
            device: Device instance

        Returns:
            bool: True if successful
        """
        try:
            logger.info("📱 Opening WhatsApp...")
            success = await device.adb.start_app(self.app_package, self.app_activity)

            if success:
                logger.success("✅ WhatsApp opened")
            else:
                logger.error("❌ Failed to open WhatsApp")

            return success

        except Exception as e:
            logger.error(f"Error opening WhatsApp: {e}")
            return False

    async def close_app(self, device: Device) -> bool:
        """
        Close WhatsApp app

        Args:
            device: Device instance

        Returns:
            bool: True if successful
        """
        try:
            logger.info("Closing WhatsApp...")
            result = await device.adb.shell_command(f"am force-stop {self.app_package}")
            success = result is not None

            if success:
                logger.success("✅ WhatsApp closed")

            return success

        except Exception as e:
            logger.error(f"Error closing WhatsApp: {e}")
            return False

    async def _find_and_open_chat(
        self,
        device: Device,
        phone_number: str,
        recipient_name: str
    ) -> bool:
        """
        Find and open chat with recipient

        Args:
            device: Device instance
            phone_number: Phone number
            recipient_name: Recipient name

        Returns:
            bool: True if successful
        """
        try:
            # Step 1: Tap on search icon or new chat button
            logger.debug("Tapping search/new chat button...")
            result = await droidrun.execute_action(
                device=device,
                natural_command="Tap on the search icon or new chat button at the top",
                verify_success=True
            )

            if not result.get("success"):
                logger.warning("⚠️ Could not find search button, trying alternative...")
                # Try tapping the floating action button (new chat)
                result = await droidrun.execute_action(
                    device=device,
                    natural_command="Tap on the green floating action button for new chat",
                    verify_success=True
                )

            # Wait for search to appear
            await human_timing.variable_delay(1, 2)

            # Step 2: Type phone number in search
            logger.debug(f"Searching for: {phone_number}")

            # Click on search field
            await droidrun.execute_action(
                device=device,
                natural_command="Tap on the search box or text input field",
                verify_success=False
            )

            await human_timing.variable_delay(0.5, 1)

            # Type phone number with human typing
            await human_typing.type_text(
                text=phone_number,
                device=device,
                add_typos=False,  # No typos for phone numbers
                speed_multiplier=1.2  # Slightly faster for numbers
            )

            # Wait for search results
            await human_timing.variable_delay(2, 3)

            # Step 3: Tap on contact from search results
            logger.debug("Opening chat...")
            result = await droidrun.execute_action(
                device=device,
                natural_command=f"Tap on the first contact in the search results",
                verify_success=True
            )

            if result.get("success"):
                logger.success(f"✅ Opened chat with {recipient_name}")
                await human_timing.variable_delay(1, 2)
                return True

            logger.error(f"❌ Failed to open chat with {recipient_name}")
            return False

        except Exception as e:
            logger.error(f"Error finding and opening chat: {e}")
            return False

    async def _send_message(self, device: Device) -> bool:
        """
        Tap the send button

        Args:
            device: Device instance

        Returns:
            bool: True if successful
        """
        try:
            logger.debug("Tapping send button...")
            result = await droidrun.execute_action(
                device=device,
                natural_command="Tap on the send button (usually a paper plane icon)",
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
        """
        Verify that message was sent successfully

        Args:
            device: Device instance

        Returns:
            dict: Verification result
        """
        try:
            # Take screenshot
            screenshot = await device.adb.take_screenshot()
            if not screenshot:
                return {"success": False, "error": "Failed to take screenshot"}

            # Analyze with LLM
            prompt = """Analyze this WhatsApp chat screenshot.

Check if the most recent message was sent successfully. Look for:
- The message appears in the chat
- Single checkmark (sent) or double checkmark (delivered)
- No error messages like "Message failed to send"

Return JSON:
{
  "success": true/false,
  "status": "sent" | "delivered" | "read" | "failed",
  "reasoning": "explanation"
}"""

            response = await puter_client._generate(
                prompt=prompt,
                model="claude-sonnet-4.5"
            )

            if response:
                import json
                if "{" in response and "}" in response:
                    start = response.find("{")
                    end = response.rfind("}") + 1
                    verification = json.loads(response[start:end])

                    return verification

            return {"success": False, "error": "Could not verify"}

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
whatsapp_agent = WhatsAppAgent()
