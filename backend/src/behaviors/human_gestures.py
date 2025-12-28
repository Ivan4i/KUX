"""Human Gestures - emulates natural swipes and taps"""

import random
import math
import asyncio
from typing import Tuple
from loguru import logger


class HumanGestures:
    """Emulates human-like gestures (taps, swipes)"""

    def __init__(self):
        """Initialize Human Gestures"""
        pass

    async def tap(
        self,
        device,
        x: int,
        y: int,
        jitter: int = 5
    ) -> bool:
        """
        Perform human-like tap

        Args:
            device: Device instance
            x: X coordinate
            y: Y coordinate
            jitter: Random offset in pixels (default: 5)

        Returns:
            bool: True if successful
        """
        try:
            # Add small random offset (humans don't tap exactly on center)
            actual_x = x + random.randint(-jitter, jitter)
            actual_y = y + random.randint(-jitter, jitter)

            # Small pre-tap delay (human reaction time)
            await asyncio.sleep(random.uniform(0.05, 0.2))

            # Perform tap
            success = await device.adb.tap(actual_x, actual_y)

            # Small post-tap delay
            await asyncio.sleep(random.uniform(0.1, 0.3))

            return success

        except Exception as e:
            logger.error(f"Error performing tap: {e}")
            return False

    async def swipe(
        self,
        device,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        duration_ms: int = None
    ) -> bool:
        """
        Perform human-like swipe with non-linear path

        Args:
            device: Device instance
            x1, y1: Start coordinates
            x2, y2: End coordinates
            duration_ms: Swipe duration in milliseconds (auto if None)

        Returns:
            bool: True if successful
        """
        try:
            # Calculate distance
            distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

            # Auto-calculate duration based on distance (more natural)
            if duration_ms is None:
                # ~500 pixels/second is natural swipe speed
                duration_ms = int((distance / 500) * 1000)
                # Add random variation
                duration_ms = int(duration_ms * random.uniform(0.8, 1.2))
                # Clamp to reasonable range
                duration_ms = max(300, min(2000, duration_ms))

            # Add slight curve to path (humans don't swipe perfectly straight)
            # For simplicity, we'll use the straight swipe with duration variation
            # In production, you might want to use multiple intermediate points

            # Pre-swipe delay
            await asyncio.sleep(random.uniform(0.1, 0.3))

            # Perform swipe
            success = await device.adb.swipe(x1, y1, x2, y2, duration_ms)

            # Post-swipe delay
            await asyncio.sleep(random.uniform(0.2, 0.5))

            return success

        except Exception as e:
            logger.error(f"Error performing swipe: {e}")
            return False

    async def scroll_down(self, device, distance: int = 500) -> bool:
        """
        Scroll down naturally

        Args:
            device: Device instance
            distance: Scroll distance in pixels

        Returns:
            bool: True if successful
        """
        # Get screen center (approximate)
        # In production, you'd get actual screen dimensions
        center_x = 540  # Assuming 1080px width
        start_y = 1500
        end_y = start_y - distance

        return await self.swipe(device, center_x, start_y, center_x, end_y)

    async def scroll_up(self, device, distance: int = 500) -> bool:
        """Scroll up naturally"""
        center_x = 540
        start_y = 500
        end_y = start_y + distance

        return await self.swipe(device, center_x, start_y, center_x, end_y)

    def get_tap_coordinates_with_offset(
        self,
        x: int,
        y: int,
        max_offset: int = 10
    ) -> Tuple[int, int]:
        """
        Get tap coordinates with random offset

        Args:
            x: Original X coordinate
            y: Original Y coordinate
            max_offset: Maximum offset in pixels

        Returns:
            tuple: (adjusted_x, adjusted_y)
        """
        offset_x = random.randint(-max_offset, max_offset)
        offset_y = random.randint(-max_offset, max_offset)

        return (x + offset_x, y + offset_y)


# Global instance
human_gestures = HumanGestures()
