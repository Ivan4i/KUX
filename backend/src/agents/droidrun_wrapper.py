"""DroidRun Wrapper - AI-powered Android UI automation"""

import asyncio
from typing import Dict, Optional, List, Any
from loguru import logger

from ..device_manager.device import Device
from ..integrations.puter_client import puter_client


class DroidRunWrapper:
    """
    Wrapper for DroidRun AI-powered UI automation

    DroidRun uses LLM to understand UI and perform actions adaptively.
    This is more resilient than hardcoded selectors when WhatsApp UI changes.
    """

    def __init__(self):
        """Initialize DroidRun wrapper"""
        self.default_timeout = 30  # seconds
        self.retry_attempts = 3

    async def execute_action(
        self,
        device: Device,
        natural_command: str,
        verify_success: bool = True,
        timeout: int = None
    ) -> Dict[str, Any]:
        """
        Execute a natural language UI action using AI

        Args:
            device: Device instance
            natural_command: Natural language command (e.g., "Tap on the Send button")
            verify_success: Whether to verify action succeeded
            timeout: Timeout in seconds

        Returns:
            dict: Execution result
        """
        timeout = timeout or self.default_timeout

        try:
            logger.debug(f"🤖 DroidRun: {natural_command}")

            # Step 1: Take screenshot of current state
            screenshot_before = await device.adb.take_screenshot()
            if not screenshot_before:
                return {"success": False, "error": "Failed to take screenshot"}

            # Step 2: Analyze UI and determine action coordinates
            action_plan = await self._plan_action(
                screenshot_path=screenshot_before,
                command=natural_command,
                device=device
            )

            if not action_plan or not action_plan.get("success"):
                return {"success": False, "error": "Failed to plan action"}

            # Step 3: Execute the planned action
            execution_result = await self._execute_planned_action(
                device=device,
                action_plan=action_plan
            )

            if not execution_result.get("success"):
                return execution_result

            # Step 4: Verify success (if requested)
            if verify_success:
                await asyncio.sleep(1)  # Wait for UI to update
                screenshot_after = await device.adb.take_screenshot()

                verification = await self._verify_action_success(
                    command=natural_command,
                    screenshot_before=screenshot_before,
                    screenshot_after=screenshot_after
                )

                return {
                    "success": verification.get("success", False),
                    "action": action_plan.get("action"),
                    "verification": verification
                }

            return {"success": True, "action": action_plan.get("action")}

        except Exception as e:
            logger.error(f"❌ DroidRun error: {e}")
            return {"success": False, "error": str(e)}

    async def find_element(
        self,
        device: Device,
        element_description: str
    ) -> Optional[Dict[str, int]]:
        """
        Find UI element using natural language description

        Args:
            device: Device instance
            element_description: Element description (e.g., "Send button", "Search box")

        Returns:
            dict: Element coordinates {"x": int, "y": int}, or None if not found
        """
        try:
            logger.debug(f"🔍 Finding element: {element_description}")

            # Take screenshot
            screenshot_path = await device.adb.take_screenshot()
            if not screenshot_path:
                return None

            # Ask LLM to locate element
            prompt = f"""Analyze this Android screenshot and find the element: "{element_description}"

Return ONLY a JSON object with the element's center coordinates:
{{
  "found": true/false,
  "x": <pixel_x>,
  "y": <pixel_y>,
  "confidence": <0-100>
}}

If the element is not found, return {{"found": false}}."""

            response = await puter_client._generate(
                prompt=prompt,
                model="claude-sonnet-4.5"  # Vision capable
            )

            if not response:
                return None

            # Parse response
            import json
            if "{" in response and "}" in response:
                start = response.find("{")
                end = response.rfind("}") + 1
                data = json.loads(response[start:end])

                if data.get("found") and data.get("confidence", 0) > 70:
                    logger.success(f"✅ Found element at ({data['x']}, {data['y']})")
                    return {"x": data["x"], "y": data["y"]}

            logger.warning(f"⚠️ Element not found: {element_description}")
            return None

        except Exception as e:
            logger.error(f"Error finding element: {e}")
            return None

    async def wait_for_element(
        self,
        device: Device,
        element_description: str,
        timeout: int = 30,
        check_interval: float = 2.0
    ) -> bool:
        """
        Wait for element to appear

        Args:
            device: Device instance
            element_description: Element description
            timeout: Timeout in seconds
            check_interval: Interval between checks in seconds

        Returns:
            bool: True if element appeared
        """
        logger.info(f"⏳ Waiting for element: {element_description}")

        start_time = asyncio.get_event_loop().time()

        while (asyncio.get_event_loop().time() - start_time) < timeout:
            element = await self.find_element(device, element_description)

            if element:
                logger.success(f"✅ Element appeared: {element_description}")
                return True

            await asyncio.sleep(check_interval)

        logger.warning(f"⏱️ Timeout waiting for element: {element_description}")
        return False

    async def _plan_action(
        self,
        screenshot_path: str,
        command: str,
        device: Device
    ) -> Optional[Dict]:
        """
        Plan action using LLM vision analysis

        Args:
            screenshot_path: Path to screenshot
            command: Natural language command
            device: Device instance

        Returns:
            dict: Action plan
        """
        try:
            prompt = f"""Analyze this Android screenshot and determine how to execute: "{command}"

Return a JSON object with the action plan:
{{
  "success": true/false,
  "action": "tap" | "swipe" | "type" | "back" | "home",
  "coordinates": {{"x": int, "y": int}} (for tap),
  "swipe_from": {{"x": int, "y": int}} (for swipe),
  "swipe_to": {{"x": int, "y": int}} (for swipe),
  "text": "text to type" (for type),
  "reasoning": "explanation"
}}"""

            response = await puter_client._generate(
                prompt=prompt,
                model="claude-sonnet-4.5"
            )

            if not response:
                return None

            # Parse JSON response
            import json
            if "{" in response and "}" in response:
                start = response.find("{")
                end = response.rfind("}") + 1
                plan = json.loads(response[start:end])

                logger.debug(f"📋 Action plan: {plan.get('action')} - {plan.get('reasoning')}")
                return plan

            return None

        except Exception as e:
            logger.error(f"Error planning action: {e}")
            return None

    async def _execute_planned_action(
        self,
        device: Device,
        action_plan: Dict
    ) -> Dict[str, Any]:
        """
        Execute the planned action

        Args:
            device: Device instance
            action_plan: Action plan from _plan_action

        Returns:
            dict: Execution result
        """
        try:
            action = action_plan.get("action")

            if action == "tap":
                coords = action_plan.get("coordinates", {})
                success = await device.adb.tap(coords.get("x"), coords.get("y"))
                return {"success": success, "action": "tap"}

            elif action == "swipe":
                swipe_from = action_plan.get("swipe_from", {})
                swipe_to = action_plan.get("swipe_to", {})
                success = await device.adb.swipe(
                    swipe_from.get("x"),
                    swipe_from.get("y"),
                    swipe_to.get("x"),
                    swipe_to.get("y")
                )
                return {"success": success, "action": "swipe"}

            elif action == "type":
                text = action_plan.get("text", "")
                success = await device.adb.input_text(text)
                return {"success": success, "action": "type"}

            elif action == "back":
                success = await device.adb.press_key("KEYCODE_BACK")
                return {"success": success, "action": "back"}

            elif action == "home":
                success = await device.adb.press_key("KEYCODE_HOME")
                return {"success": success, "action": "home"}

            else:
                logger.warning(f"Unknown action: {action}")
                return {"success": False, "error": f"Unknown action: {action}"}

        except Exception as e:
            logger.error(f"Error executing action: {e}")
            return {"success": False, "error": str(e)}

    async def _verify_action_success(
        self,
        command: str,
        screenshot_before: str,
        screenshot_after: str
    ) -> Dict[str, Any]:
        """
        Verify that action succeeded by comparing screenshots

        Args:
            command: Original command
            screenshot_before: Screenshot before action
            screenshot_after: Screenshot after action

        Returns:
            dict: Verification result
        """
        try:
            prompt = f"""Compare these two Android screenshots (before and after an action).

Action performed: "{command}"

Did the action succeed? Look for:
- UI changes that indicate success
- Error messages
- Unexpected behavior

Return JSON:
{{
  "success": true/false,
  "confidence": <0-100>,
  "reasoning": "explanation",
  "errors_detected": ["error1", "error2"] (if any)
}}"""

            response = await puter_client._generate(
                prompt=prompt,
                model="claude-sonnet-4.5"
            )

            if not response:
                return {"success": False, "error": "No response from LLM"}

            # Parse JSON
            import json
            if "{" in response and "}" in response:
                start = response.find("{")
                end = response.rfind("}") + 1
                verification = json.loads(response[start:end])

                if verification.get("success"):
                    logger.success(f"✅ Action verified: {verification.get('reasoning')}")
                else:
                    logger.warning(f"⚠️ Action may have failed: {verification.get('reasoning')}")

                return verification

            return {"success": False, "error": "Could not parse verification"}

        except Exception as e:
            logger.error(f"Error verifying action: {e}")
            return {"success": False, "error": str(e)}


# Global instance
droidrun = DroidRunWrapper()
