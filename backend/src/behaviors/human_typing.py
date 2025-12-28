"""Human Typing Emulation - types text like a real person"""

import asyncio
import random
from typing import Optional
from loguru import logger


class HumanTyping:
    """Emulates human typing behavior"""

    def __init__(self):
        """Initialize Human Typing"""
        self.average_chars_per_minute = 80  # Realistic typing speed
        self.typo_rate = 0.05  # 5% chance of typo
        self.pause_rate = 0.02  # 2% chance of pause mid-word

    async def type_text(
        self,
        text: str,
        device,
        add_typos: bool = False,
        speed_multiplier: float = 1.0
    ) -> bool:
        """
        Type text character by character with human-like timing

        Args:
            text: Text to type
            device: Device instance with input_text method
            add_typos: Whether to add realistic typos
            speed_multiplier: Speed multiplier (1.0 = normal, 0.5 = slower, 2.0 = faster)

        Returns:
            bool: True if successful
        """
        try:
            logger.debug(f"Typing text: '{text[:50]}{'...' if len(text) > 50 else ''}'")

            # Calculate base delay between characters
            base_delay = (60.0 / self.average_chars_per_minute) / speed_multiplier

            words = text.split(' ')

            for word_index, word in enumerate(words):
                for char_index, char in enumerate(word):
                    # Gaussian distribution for natural variation
                    char_delay = max(0.01, random.gauss(base_delay, base_delay * 0.3))

                    # Occasional typo
                    if add_typos and random.random() < self.typo_rate:
                        await self._make_typo(device, char)
                        # Extra delay after correction
                        await asyncio.sleep(random.uniform(0.2, 0.5))

                    # Type the character
                    await device.adb.input_text(char)
                    await asyncio.sleep(char_delay)

                    # Occasional thinking pause mid-word
                    if random.random() < self.pause_rate:
                        thinking_pause = random.uniform(0.5, 2.0)
                        logger.debug(f"Thinking pause: {thinking_pause:.2f}s")
                        await asyncio.sleep(thinking_pause)

                # Space between words
                if word_index < len(words) - 1:
                    await device.adb.input_text(' ')
                    space_delay = random.gauss(base_delay * 1.5, base_delay * 0.5)
                    await asyncio.sleep(max(0.01, space_delay))

            logger.debug("✅ Finished typing text")
            return True

        except Exception as e:
            logger.error(f"Error typing text: {e}")
            return False

    async def _make_typo(self, device, correct_char: str):
        """
        Make a typo and correct it

        Args:
            device: Device instance
            correct_char: The correct character
        """
        try:
            # Common typo: adjacent key on keyboard
            typo_chars = self._get_adjacent_keys(correct_char)

            if typo_chars:
                wrong_char = random.choice(typo_chars)
                logger.debug(f"Typo: '{wrong_char}' instead of '{correct_char}'")

                # Type wrong character
                await device.adb.input_text(wrong_char)
                await asyncio.sleep(random.uniform(0.1, 0.3))

                # Realize mistake, pause
                await asyncio.sleep(random.uniform(0.2, 0.6))

                # Backspace
                await device.adb.press_key('KEYCODE_DEL')
                await asyncio.sleep(random.uniform(0.1, 0.2))

        except Exception as e:
            logger.error(f"Error making typo: {e}")

    def _get_adjacent_keys(self, char: str) -> list:
        """
        Get adjacent keys on QWERTY keyboard

        Args:
            char: Character

        Returns:
            list: List of adjacent characters
        """
        # Simplified keyboard layout (QWERTY)
        keyboard = {
            'a': ['q', 's', 'z'],
            'b': ['v', 'g', 'n'],
            'c': ['x', 'd', 'v'],
            'd': ['s', 'e', 'f', 'c'],
            'e': ['w', 'r', 'd'],
            'f': ['d', 'r', 'g', 'v'],
            'g': ['f', 't', 'h', 'b'],
            'h': ['g', 'y', 'j', 'n'],
            'i': ['u', 'o', 'k'],
            'j': ['h', 'u', 'k', 'm'],
            'k': ['j', 'i', 'l'],
            'l': ['k', 'o', 'p'],
            'm': ['n', 'j', 'k'],
            'n': ['b', 'h', 'm'],
            'o': ['i', 'p', 'l'],
            'p': ['o', 'l'],
            'q': ['w', 'a'],
            'r': ['e', 't', 'f'],
            's': ['a', 'w', 'd', 'x'],
            't': ['r', 'y', 'g'],
            'u': ['y', 'i', 'j'],
            'v': ['c', 'f', 'b'],
            'w': ['q', 'e', 's'],
            'x': ['z', 's', 'c'],
            'y': ['t', 'u', 'h'],
            'z': ['a', 'x']
        }

        return keyboard.get(char.lower(), [])

    def calculate_typing_duration(self, text: str, speed_multiplier: float = 1.0) -> float:
        """
        Calculate approximate typing duration

        Args:
            text: Text to type
            speed_multiplier: Speed multiplier

        Returns:
            float: Estimated duration in seconds
        """
        char_count = len(text)
        base_duration = (char_count / self.average_chars_per_minute) * 60
        adjusted_duration = base_duration / speed_multiplier

        # Add some overhead for typos and pauses
        overhead = adjusted_duration * 0.15  # 15% overhead

        return adjusted_duration + overhead


# Global instance
human_typing = HumanTyping()
