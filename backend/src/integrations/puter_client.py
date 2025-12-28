"""Puter.js LLM API Client - manages AI model requests"""

import asyncio
from typing import Optional, Dict, List
import httpx
from loguru import logger

from ..config import get_settings


class PuterClient:
    """Manages integration with Puter.js LLM API"""

    def __init__(self):
        """Initialize Puter.js client"""
        settings = get_settings()
        self.api_key = settings.puter_api_key
        self.api_url = settings.puter_api_url
        self.default_model = settings.puter_default_model
        self.timeout = 60.0  # 60 seconds timeout for LLM requests

        # Simple cache for responses (to avoid redundant API calls)
        self._cache: Dict[str, str] = {}

        # Available models
        self.available_models = [
            "claude-sonnet-4.5",
            "gemini-3-pro",
            "gpt-5.1"
        ]

    async def generate_message(
        self,
        recipient_name: str,
        context: Optional[str] = None,
        template: Optional[str] = None,
        model: Optional[str] = None,
        use_cache: bool = True
    ) -> Optional[str]:
        """
        Generate personalized WhatsApp message using LLM

        Args:
            recipient_name: Name of the recipient
            context: Additional context about recipient (job title, company, etc.)
            template: Optional message template
            model: LLM model to use (CRITICAL: always specify!)
            use_cache: Whether to use cached responses

        Returns:
            str: Generated message, or None if failed
        """
        try:
            # Check cache
            cache_key = f"msg:{recipient_name}:{context}:{template}"
            if use_cache and cache_key in self._cache:
                logger.debug(f"Using cached message for {recipient_name}")
                return self._cache[cache_key]

            # Build prompt
            prompt = self._build_message_prompt(recipient_name, context, template)

            # Generate using LLM (CRITICAL: always pass model!)
            model = model or self.default_model
            response = await self._generate(prompt, model=model)

            if response:
                # Cache the response
                self._cache[cache_key] = response
                logger.success(f"✅ Generated message for {recipient_name} using {model}")
                return response

            return None

        except Exception as e:
            logger.error(f"❌ Error generating message: {e}")
            return None

    async def analyze_screenshot(
        self,
        screenshot_path: str,
        analysis_type: str = "ui_elements",
        model: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Analyze screenshot using vision-capable LLM

        Args:
            screenshot_path: Path to screenshot image
            analysis_type: Type of analysis ("ui_elements", "error_detection", "state_check")
            model: LLM model to use (CRITICAL: always specify!)

        Returns:
            dict: Analysis results with structured data
        """
        try:
            logger.info(f"🔍 Analyzing screenshot: {screenshot_path}")

            # Build prompt based on analysis type
            prompt = self._build_analysis_prompt(analysis_type)

            # Use vision-capable model (CRITICAL: always pass model!)
            model = model or "claude-sonnet-4.5"  # Claude has vision

            # For now, we'll use text-only API
            # TODO: Implement multimodal API when Puter.js supports it
            response = await self._generate(prompt, model=model)

            if response:
                logger.success(f"✅ Screenshot analysis completed using {model}")
                # Parse response into structured format
                return self._parse_analysis_response(response)

            return None

        except Exception as e:
            logger.error(f"❌ Error analyzing screenshot: {e}")
            return None

    async def suggest_recovery_action(
        self,
        error_message: str,
        screenshot_path: Optional[str] = None,
        previous_attempts: List[str] = None,
        model: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Suggest recovery action for error using LLM

        Args:
            error_message: Error message or description
            screenshot_path: Optional screenshot of error state
            previous_attempts: List of previously attempted recovery actions
            model: LLM model to use (CRITICAL: always specify!)

        Returns:
            dict: Recovery suggestion with action type and parameters
        """
        try:
            logger.info(f"🤔 Requesting recovery suggestion for: {error_message[:100]}")

            # Build prompt
            prompt = self._build_recovery_prompt(
                error_message,
                screenshot_path,
                previous_attempts or []
            )

            # Generate using LLM (CRITICAL: always pass model!)
            model = model or self.default_model
            response = await self._generate(prompt, model=model)

            if response:
                logger.success(f"✅ Recovery suggestion generated using {model}")
                return self._parse_recovery_response(response)

            return None

        except Exception as e:
            logger.error(f"❌ Error generating recovery suggestion: {e}")
            return None

    async def _generate(
        self,
        prompt: str,
        model: str,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> Optional[str]:
        """
        Core method to generate LLM response

        Args:
            prompt: Prompt text
            model: Model name (CRITICAL: MUST be specified!)
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature

        Returns:
            str: Generated text, or None if failed
        """
        try:
            # CRITICAL: Validate that model is explicitly specified
            if not model or model not in self.available_models:
                logger.warning(
                    f"⚠️ Model '{model}' not in available models. "
                    f"Using default: {self.default_model}"
                )
                model = self.default_model

            logger.debug(f"Sending request to Puter.js API with model: {model}")

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.api_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,  # CRITICAL: Always include model!
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "max_tokens": max_tokens,
                        "temperature": temperature
                    }
                )

                response.raise_for_status()
                data = response.json()

                # Extract generated text
                generated_text = data.get("choices", [{}])[0].get("message", {}).get("content", "")

                if generated_text:
                    logger.debug(f"Generated {len(generated_text)} characters using {model}")
                    return generated_text.strip()

                logger.warning("⚠️ Empty response from LLM")
                return None

        except httpx.HTTPStatusError as e:
            logger.error(f"❌ HTTP error from Puter.js API: {e.response.status_code} - {e.response.text}")
            return None
        except httpx.TimeoutException:
            logger.error(f"❌ Timeout waiting for LLM response (>{self.timeout}s)")
            return None
        except Exception as e:
            logger.error(f"❌ Unexpected error calling Puter.js API: {e}")
            return None

    def _build_message_prompt(
        self,
        recipient_name: str,
        context: Optional[str],
        template: Optional[str]
    ) -> str:
        """Build prompt for message generation"""

        base_prompt = f"""Generate a personalized, professional WhatsApp message for outreach.

Recipient: {recipient_name}"""

        if context:
            base_prompt += f"\nContext: {context}"

        if template:
            base_prompt += f"\n\nTemplate to follow:\n{template}"
        else:
            base_prompt += """

The message should:
- Be friendly and professional
- Be concise (2-3 sentences max)
- Have a clear call-to-action
- Feel natural and human-written (not robotic)
- Be appropriate for WhatsApp (informal tone is OK)

Only return the message text, nothing else."""

        return base_prompt

    def _build_analysis_prompt(self, analysis_type: str) -> str:
        """Build prompt for screenshot analysis"""

        prompts = {
            "ui_elements": """Analyze this screenshot and identify all interactive UI elements.
For each element, provide:
- Element type (button, input field, text, etc.)
- Text content (if visible)
- Approximate position (top/middle/bottom, left/center/right)
- Whether it's clickable

Return as structured JSON.""",

            "error_detection": """Analyze this screenshot for any error messages or warning indicators.
Look for:
- Error dialogs or popups
- Warning icons
- "Failed" or "Error" text
- Network connectivity issues
- App crashes

Return as structured JSON with error details.""",

            "state_check": """Analyze this screenshot to determine the current app state.
Identify:
- Which screen/view is currently shown
- Whether the app is ready for input
- If any loading indicators are visible
- If there are any blocking modals

Return as structured JSON."""
        }

        return prompts.get(analysis_type, prompts["ui_elements"])

    def _build_recovery_prompt(
        self,
        error_message: str,
        screenshot_path: Optional[str],
        previous_attempts: List[str]
    ) -> str:
        """Build prompt for recovery suggestion"""

        prompt = f"""An automation task failed with the following error:

Error: {error_message}"""

        if screenshot_path:
            prompt += f"\nScreenshot available at: {screenshot_path}"

        if previous_attempts:
            prompt += f"\n\nPrevious recovery attempts (all failed):\n"
            for i, attempt in enumerate(previous_attempts, 1):
                prompt += f"{i}. {attempt}\n"

        prompt += """

Suggest the best recovery action. Choose from these options:
1. "retry_simple" - Just retry the same action
2. "alternative_path" - Try a different UI approach (suggest specific steps)
3. "restart_app" - Close and restart the application
4. "reboot_device" - Reboot the device
5. "manual_intervention" - Requires human assistance

Return as JSON with:
{
  "action": "action_type",
  "reason": "explanation",
  "steps": ["step 1", "step 2", ...] (if applicable)
}"""

        return prompt

    def _parse_analysis_response(self, response: str) -> Dict:
        """Parse LLM analysis response into structured format"""
        try:
            # Try to extract JSON from response
            import json

            # Simple extraction (assumes LLM returns JSON)
            # TODO: More robust parsing with regex if needed
            if "{" in response and "}" in response:
                start = response.find("{")
                end = response.rfind("}") + 1
                json_str = response[start:end]
                return json.loads(json_str)

            # Fallback: return raw text
            return {"raw_analysis": response}

        except Exception as e:
            logger.warning(f"Could not parse analysis as JSON: {e}")
            return {"raw_analysis": response}

    def _parse_recovery_response(self, response: str) -> Dict:
        """Parse LLM recovery suggestion into structured format"""
        try:
            import json

            # Extract JSON from response
            if "{" in response and "}" in response:
                start = response.find("{")
                end = response.rfind("}") + 1
                json_str = response[start:end]
                return json.loads(json_str)

            # Fallback: simple retry
            return {
                "action": "retry_simple",
                "reason": "Could not parse LLM response",
                "steps": []
            }

        except Exception as e:
            logger.warning(f"Could not parse recovery suggestion as JSON: {e}")
            return {
                "action": "retry_simple",
                "reason": "Parsing error",
                "steps": []
            }

    def clear_cache(self):
        """Clear response cache"""
        self._cache.clear()
        logger.info("🗑️ Cleared Puter.js response cache")


# Global instance
puter_client = PuterClient()
