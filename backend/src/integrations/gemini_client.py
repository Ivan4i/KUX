"""LLM Client via OpenRouter - manages AI model requests for lead analysis and message generation"""

import asyncio
import base64
import hashlib
import json
from pathlib import Path
from typing import Optional, Dict, List, Any
import httpx
from loguru import logger

from ..config import get_settings


class GeminiClient:
    """Manages LLM integration via OpenRouter API for lead analysis and message generation"""

    def __init__(self):
        """Initialize LLM client with OpenRouter"""
        settings = get_settings()
        self.api_key = settings.openrouter_api_key
        self.base_url = settings.openrouter_base_url
        self.model_name = settings.llm_model
        self.vision_model_name = settings.llm_vision_model
        self.timeout = settings.llm_timeout
        self.context_dir = Path(settings.llm_context_dir)

        # Response cache
        self._cache: Dict[str, Any] = {}

        # Context cache (for .md files)
        self._context_cache: Optional[str] = None
        self._context_hash: Optional[str] = None

        if self.api_key:
            logger.success(f"✅ LLM client initialized with OpenRouter, model: {self.model_name}")
        else:
            logger.warning("⚠️ OpenRouter API key not configured")

    def is_available(self) -> bool:
        """Check if LLM client is properly initialized"""
        return bool(self.api_key)

    async def _call_openrouter(
        self,
        messages: List[Dict[str, Any]],
        model: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.7
    ) -> Optional[str]:
        """Make API call to OpenRouter"""
        if not self.is_available():
            logger.warning("⚠️ OpenRouter API key not configured")
            return None

        model = model or self.model_name

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://kux.local",
                        "X-Title": "KUX Android Agent Platform"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "max_tokens": max_tokens,
                        "temperature": temperature
                    }
                )

                response.raise_for_status()
                data = response.json()

                # Extract content
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")

                if content:
                    logger.debug(f"Generated {len(content)} characters using {model}")
                    return content.strip()

                logger.warning("⚠️ Empty response from LLM")
                return None

        except httpx.HTTPStatusError as e:
            logger.error(f"❌ HTTP error from OpenRouter: {e.response.status_code} - {e.response.text}")
            return None
        except httpx.TimeoutException:
            logger.error(f"❌ Timeout waiting for LLM response (>{self.timeout}s)")
            return None
        except Exception as e:
            logger.error(f"❌ Error calling OpenRouter: {e}")
            return None

    async def load_context_files(self) -> str:
        """Load all .md context files from context directory"""
        try:
            if not self.context_dir.exists():
                logger.warning(f"⚠️ Context directory not found: {self.context_dir}")
                return ""

            md_files = sorted(self.context_dir.glob("*.md"))

            if not md_files:
                logger.warning(f"⚠️ No .md files found in {self.context_dir}")
                return ""

            context_parts = []
            for md_file in md_files:
                content = md_file.read_text(encoding="utf-8")
                context_parts.append(f"# {md_file.stem}\n\n{content}")

            combined_context = "\n\n---\n\n".join(context_parts)

            new_hash = hashlib.md5(combined_context.encode()).hexdigest()

            if new_hash != self._context_hash:
                self._context_cache = combined_context
                self._context_hash = new_hash
                logger.info(f"📚 Loaded {len(md_files)} context files ({len(combined_context)} chars)")

            return self._context_cache

        except Exception as e:
            logger.error(f"❌ Error loading context files: {e}")
            return ""

    async def analyze_lead(
        self,
        lead_data: Dict[str, Any],
        use_context: bool = True
    ) -> Dict[str, Any]:
        """Analyze lead and generate personalized message"""
        if not self.is_available():
            logger.warning("⚠️ LLM not available, using fallback template")
            return self._fallback_message(lead_data)

        try:
            cache_key = f"lead:{lead_data.get('name', '')}:{lead_data.get('company', '')}"
            if cache_key in self._cache:
                logger.debug(f"Using cached analysis for {lead_data.get('name')}")
                return self._cache[cache_key]

            context = ""
            if use_context:
                context = await self.load_context_files()

            prompt = self._build_analysis_prompt(lead_data, context)

            messages = [{"role": "user", "content": prompt}]
            response = await self._call_openrouter(messages)

            result = self._parse_analysis_response(response, lead_data)

            self._cache[cache_key] = result

            logger.success(f"✅ Analyzed lead: {lead_data.get('name')} (confidence: {result.get('confidence')}%)")
            return result

        except Exception as e:
            logger.error(f"❌ Error analyzing lead: {e}")
            return self._fallback_message(lead_data)

    async def analyze_screenshot(
        self,
        screenshot_path: str,
        analysis_type: str = "ui_elements"
    ) -> Optional[Dict]:
        """Analyze screenshot using vision-capable LLM"""
        if not self.is_available():
            logger.warning("⚠️ LLM not available")
            return None

        try:
            image_path = Path(screenshot_path)
            if not image_path.exists():
                logger.error(f"❌ Screenshot not found: {screenshot_path}")
                return None

            image_data = image_path.read_bytes()
            base64_image = base64.b64encode(image_data).decode("utf-8")

            # Determine MIME type
            suffix = image_path.suffix.lower()
            mime_type = {
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".webp": "image/webp"
            }.get(suffix, "image/png")

            prompt = self._build_vision_prompt(analysis_type)

            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]

            response = await self._call_openrouter(
                messages,
                model=self.vision_model_name,
                temperature=0.3
            )

            result = self._parse_json_response(response) if response else None

            logger.success(f"✅ Screenshot analyzed: {analysis_type}")
            return result

        except Exception as e:
            logger.error(f"❌ Error analyzing screenshot: {e}")
            return None

    async def suggest_recovery(
        self,
        error_message: str,
        screenshot_path: Optional[str] = None,
        previous_attempts: List[str] = None
    ) -> Dict[str, Any]:
        """Suggest recovery action for failed automation step"""
        if not self.is_available():
            return {
                "action": "retry_simple",
                "reason": "LLM not available",
                "steps": []
            }

        try:
            prompt = self._build_recovery_prompt(
                error_message,
                screenshot_path,
                previous_attempts or []
            )

            messages = [{"role": "user", "content": prompt}]
            response = await self._call_openrouter(messages, temperature=0.5)

            result = self._parse_json_response(response) if response else {}

            if "action" not in result:
                result["action"] = "retry_simple"
            if "reason" not in result:
                result["reason"] = "Unknown"
            if "steps" not in result:
                result["steps"] = []

            logger.info(f"🔧 Recovery suggestion: {result['action']}")
            return result

        except Exception as e:
            logger.error(f"❌ Error getting recovery suggestion: {e}")
            return {
                "action": "retry_simple",
                "reason": f"Error: {str(e)}",
                "steps": []
            }

    async def generate_message(
        self,
        recipient_name: str,
        context: Optional[str] = None,
        template: Optional[str] = None
    ) -> Optional[str]:
        """Generate personalized message for recipient"""
        if not self.is_available():
            return None

        try:
            prompt = f"""Сгенерируй персонализированное деловое сообщение.

Получатель: {recipient_name}
"""
            if context:
                prompt += f"Контекст: {context}\n"

            if template:
                prompt += f"\nШаблон:\n{template}\n"

            prompt += """
Требования:
- Короткое сообщение (2-3 предложения)
- Деловой тон
- Выглядит как от реального человека
- Только текст сообщения, без пояснений
"""

            messages = [{"role": "user", "content": prompt}]
            response = await self._call_openrouter(messages, temperature=0.8)

            return response

        except Exception as e:
            logger.error(f"❌ Error generating message: {e}")
            return None

    def _build_analysis_prompt(self, lead_data: Dict, context: str) -> str:
        """Build prompt for lead analysis and message generation"""

        prompt = """Ты - эксперт по B2B продажам в России. Проанализируй данные лида и сгенерируй персонализированное сообщение.

"""

        if context:
            prompt += f"""КОНТЕКСТ (правила написания сообщений, примеры, методология):
{context}

---

"""

        prompt += f"""ДАННЫЕ ЛИДА:
- Имя: {lead_data.get('name', 'Неизвестно')}
- Компания: {lead_data.get('company', 'Неизвестно')}
- Сайт: {lead_data.get('website', 'Нет данных')}
- RusProfile: {lead_data.get('rusprofile_url', 'Нет данных')}
- Выручка: {lead_data.get('revenue', 'Нет данных')} руб/год
- Прибыль: {lead_data.get('profit', 'Нет данных')} руб/год
- Телефон: {lead_data.get('phone', 'Нет')}

ЗАДАЧА:
1. Проанализируй бизнес лида
2. Сгенерируй короткое персонализированное сообщение (2-3 предложения)
3. Сообщение должно выглядеть как от реального человека, не как шаблон
4. Упомяни что-то конкретное о компании/выручке/бизнесе

ВЕРНИ ОТВЕТ В JSON:
{{
  "message": "Текст сообщения здесь",
  "confidence": 85,
  "flags": [],
  "tone": "professional",
  "analysis": "Краткий анализ бизнеса"
}}

Если данных недостаточно для персонализации, укажи confidence < 50 и добавь flag "insufficient_data".
"""

        return prompt

    def _build_vision_prompt(self, analysis_type: str) -> str:
        """Build prompt for screenshot analysis"""

        prompts = {
            "ui_elements": """Analyze this Android app screenshot. Identify all interactive UI elements.

For each element, provide:
- type: button, input_field, text, icon, image, checkbox, etc.
- text: visible text (if any)
- position: approximate position (top/middle/bottom, left/center/right)
- clickable: true/false
- bounds: approximate coordinates [x1, y1, x2, y2]

Return as JSON:
{
  "elements": [
    {"type": "button", "text": "Send", "position": "bottom-right", "clickable": true, "bounds": [800, 1600, 1000, 1700]}
  ],
  "current_screen": "chat_window",
  "app_name": "WhatsApp"
}""",

            "error_detection": """Analyze this Android app screenshot for errors or problems.

Look for:
- Error dialogs or popups
- Warning icons
- "Failed", "Error", "Ошибка" text
- Network issues
- App crashes
- Captcha or verification requests

Return as JSON:
{
  "has_error": true/false,
  "error_type": "dialog" | "network" | "captcha" | "crash" | null,
  "error_message": "visible error text",
  "blocking": true/false,
  "suggested_action": "dismiss_dialog" | "retry" | "wait" | "manual"
}""",

            "state_check": """Analyze this Android app screenshot to determine current state.

Identify:
- Which screen/view is shown
- Is app ready for input?
- Any loading indicators?
- Any blocking modals?
- Is keyboard visible?

Return as JSON:
{
  "screen": "main_chat" | "contact_list" | "search" | "settings" | "unknown",
  "ready_for_input": true/false,
  "is_loading": true/false,
  "has_modal": true/false,
  "keyboard_visible": true/false,
  "suggested_action": "proceed" | "wait" | "dismiss" | "scroll"
}"""
        }

        return prompts.get(analysis_type, prompts["ui_elements"])

    def _build_recovery_prompt(
        self,
        error_message: str,
        screenshot_path: Optional[str],
        previous_attempts: List[str]
    ) -> str:
        """Build prompt for recovery suggestion"""

        prompt = f"""Automation task failed. Suggest recovery action.

ERROR: {error_message}
"""

        if previous_attempts:
            prompt += "\nPREVIOUS FAILED ATTEMPTS:\n"
            for i, attempt in enumerate(previous_attempts, 1):
                prompt += f"{i}. {attempt}\n"

        prompt += """
AVAILABLE RECOVERY ACTIONS:
1. "retry_simple" - Retry same action
2. "alternative_path" - Try different UI approach
3. "restart_app" - Close and restart app
4. "reboot_device" - Reboot device
5. "skip_contact" - Skip this contact, continue with next
6. "manual_intervention" - Requires human help

Return as JSON:
{
  "action": "action_type",
  "reason": "why this action",
  "steps": ["step1", "step2"] (if applicable),
  "wait_seconds": 0 (if should wait before action)
}
"""

        return prompt

    def _parse_analysis_response(self, response_text: Optional[str], lead_data: Dict) -> Dict[str, Any]:
        """Parse LLM response for lead analysis"""
        if not response_text:
            return self._fallback_message(lead_data)

        try:
            result = self._parse_json_response(response_text)

            if "message" not in result or not result["message"]:
                result = self._fallback_message(lead_data)

            if "confidence" not in result:
                result["confidence"] = 70

            if "flags" not in result:
                result["flags"] = []

            if "tone" not in result:
                result["tone"] = "professional"

            return result

        except Exception as e:
            logger.warning(f"Could not parse analysis response: {e}")
            return self._fallback_message(lead_data)

    def _parse_json_response(self, response_text: str) -> Dict:
        """Extract and parse JSON from response"""
        try:
            text = response_text.strip()

            # Try to find JSON block
            if "```json" in text:
                start = text.find("```json") + 7
                end = text.find("```", start)
                text = text[start:end].strip()
            elif "```" in text:
                start = text.find("```") + 3
                end = text.find("```", start)
                text = text[start:end].strip()

            # Try to find raw JSON
            if text.startswith("{"):
                end = text.rfind("}") + 1
                text = text[:end]

            return json.loads(text)

        except json.JSONDecodeError as e:
            logger.warning(f"JSON parse error: {e}")
            return {"raw_response": response_text}

    def _fallback_message(self, lead_data: Dict) -> Dict[str, Any]:
        """Generate fallback message when LLM fails"""
        name = lead_data.get("name", "").split()[0] if lead_data.get("name") else "Здравствуйте"
        company = lead_data.get("company", "вашей компании")

        message = f"{name}, добрый день! Нашел информацию о {company} и хотел бы обсудить возможное сотрудничество. Когда удобно созвониться?"

        return {
            "message": message,
            "confidence": 40,
            "flags": ["fallback_template"],
            "tone": "professional",
            "analysis": "Fallback template used due to insufficient data or API error"
        }

    def clear_cache(self):
        """Clear all caches"""
        self._cache.clear()
        self._context_cache = None
        self._context_hash = None
        logger.info("🗑️ Cleared LLM caches")


# Global instance
gemini_client = GeminiClient()
