"""Human Timing - controls delays and schedules like a real person"""

import random
import asyncio
from datetime import datetime, time
from typing import Tuple
import pytz
from loguru import logger


class HumanTiming:
    """Emulates human timing patterns"""

    def __init__(self):
        """Initialize Human Timing"""
        self.default_min_delay = 15 * 60  # 15 minutes in seconds
        self.default_max_delay = 25 * 60  # 25 minutes in seconds

    def get_random_delay(
        self,
        min_seconds: float,
        max_seconds: float,
        distribution: str = "gaussian"
    ) -> float:
        """
        Get random delay with specified distribution

        Args:
            min_seconds: Minimum delay
            max_seconds: Maximum delay
            distribution: 'gaussian' or 'uniform'

        Returns:
            float: Delay in seconds
        """
        if distribution == "gaussian":
            # Gaussian distribution feels more natural
            mean = (min_seconds + max_seconds) / 2
            std_dev = (max_seconds - min_seconds) / 4

            delay = random.gauss(mean, std_dev)

            # Clamp to bounds
            delay = max(min_seconds, min(max_seconds, delay))

        else:
            # Uniform distribution
            delay = random.uniform(min_seconds, max_seconds)

        return delay

    def get_message_interval(
        self,
        account_age_days: int,
        warmup_mode: bool = True
    ) -> Tuple[float, float]:
        """
        Get appropriate interval between messages based on account age

        Args:
            account_age_days: Age of WhatsApp account in days
            warmup_mode: Whether to use warmup mode for new accounts

        Returns:
            tuple: (min_seconds, max_seconds)
        """
        if warmup_mode and account_age_days < 7:
            # New account: very conservative
            # Wait longer between messages (30-60 minutes)
            logger.info(f"🔥 Warmup mode: Account age {account_age_days} days")
            return (30 * 60, 60 * 60)

        elif account_age_days < 14:
            # Still being careful (20-40 minutes)
            return (20 * 60, 40 * 60)

        else:
            # Normal mode (15-25 minutes)
            return (self.default_min_delay, self.default_max_delay)

    def should_be_active_now(
        self,
        timezone_str: str,
        active_hours: str = "08:00-22:00",
        account_age_days: int = 30
    ) -> bool:
        """
        Check if agent should be active at current time

        Args:
            timezone_str: Timezone (e.g., "Asia/Bangkok")
            active_hours: Active hours range (e.g., "08:00-22:00")
            account_age_days: Account age in days

        Returns:
            bool: True if should be active
        """
        try:
            # Get current time in device timezone
            tz = pytz.timezone(timezone_str)
            current_time = datetime.now(tz)

            # Parse active hours
            start_str, end_str = active_hours.split('-')
            start_hour, start_min = map(int, start_str.split(':'))
            end_hour, end_min = map(int, end_str.split(':'))

            start_time = time(start_hour, start_min)
            end_time = time(end_hour, end_min)

            current_time_only = current_time.time()

            # Check if within active hours
            if not (start_time <= current_time_only <= end_time):
                logger.debug(f"Outside active hours: {current_time_only}")
                return False

            # Check day of week
            day_of_week = current_time.weekday()  # 0 = Monday, 6 = Sunday

            # Weekend slowdown
            if day_of_week >= 5:  # Saturday or Sunday
                # 50% chance of being active on weekends
                if random.random() > 0.5:
                    logger.debug("Weekend slowdown: skipping activity")
                    return False

            # Warmup mode for new accounts
            if account_age_days < 7:
                # Limit to 5 messages per day
                # Distribute activity throughout the day
                # Simplified: 5 messages over ~14 hours = ~35% activity rate
                if random.random() > 0.35:
                    logger.debug("Warmup mode: skipping activity")
                    return False

            return True

        except Exception as e:
            logger.error(f"Error checking active time: {e}")
            return True  # Default to active if error

    def get_cooldown_period(self, messages_sent: int) -> float:
        """
        Get cooldown period after sending messages

        Args:
            messages_sent: Number of messages sent in current batch

        Returns:
            float: Cooldown period in seconds
        """
        if messages_sent >= 10:
            # Long cooldown after 10 messages (1-2 hours)
            return random.uniform(60 * 60, 120 * 60)
        elif messages_sent >= 5:
            # Medium cooldown after 5 messages (30-60 minutes)
            return random.uniform(30 * 60, 60 * 60)
        else:
            # Short cooldown (10-20 minutes)
            return random.uniform(10 * 60, 20 * 60)

    def get_think_delay(self) -> float:
        """
        Get delay for "thinking" (reading message, deciding what to write)

        Returns:
            float: Delay in seconds (5-15 seconds)
        """
        return random.uniform(5.0, 15.0)

    def get_ui_navigation_delay(self) -> float:
        """
        Get delay for UI navigation (opening app, finding contact)

        Returns:
            float: Delay in seconds (2-5 seconds)
        """
        return random.uniform(2.0, 5.0)

    async def variable_delay(self, min_seconds: float, max_seconds: float) -> None:
        """
        Add random delay between min and max seconds

        Args:
            min_seconds: Minimum delay in seconds
            max_seconds: Maximum delay in seconds
        """
        delay = random.uniform(min_seconds, max_seconds)
        logger.debug(f"⏱️ Variable delay: {delay:.2f}s")
        await asyncio.sleep(delay)


# Global instance
human_timing = HumanTiming()
