"""Rate Limit Service - manages per-device rate limiting for message sending"""

import asyncio
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import RateLimit, Device


class RateLimitService:
    """Manages rate limiting for message sending across devices and channels"""

    # Default limits per channel
    DEFAULT_LIMITS = {
        "whatsapp": {"max_per_hour": 15, "max_per_day": 80, "min_interval": 120},
        "sms": {"max_per_hour": 30, "max_per_day": 200, "min_interval": 30},
        "max": {"max_per_hour": 20, "max_per_day": 100, "min_interval": 60},
        "telegram": {"max_per_hour": 25, "max_per_day": 150, "min_interval": 45},
        "global": {"max_per_hour": 50, "max_per_day": 300, "min_interval": 30}
    }

    def __init__(self):
        """Initialize rate limit service"""
        # In-memory cache for fast lookups (synced with DB)
        self._cache: Dict[str, Dict] = {}
        logger.info("⏱️ Rate limit service initialized")

    def _get_cache_key(self, device_id: str, channel: str) -> str:
        """Generate cache key for device+channel combination"""
        return f"{device_id}:{channel}"

    async def get_or_create_limit(
        self,
        db: AsyncSession,
        device_id: str,
        channel: str
    ) -> RateLimit:
        """
        Get or create rate limit record for device+channel.

        Args:
            db: Database session
            device_id: Device identifier
            channel: Channel type (whatsapp, sms, max, etc.)

        Returns:
            RateLimit model instance
        """
        # Check cache first
        cache_key = self._get_cache_key(device_id, channel)

        # Query database
        result = await db.execute(
            select(RateLimit).where(
                RateLimit.device_id == device_id,
                RateLimit.limit_type == channel
            )
        )
        rate_limit = result.scalar_one_or_none()

        if not rate_limit:
            # Create new rate limit with defaults
            defaults = self.DEFAULT_LIMITS.get(channel, self.DEFAULT_LIMITS["global"])
            rate_limit = RateLimit(
                device_id=device_id,
                limit_type=channel,
                max_per_hour=defaults["max_per_hour"],
                max_per_day=defaults["max_per_day"],
                min_interval_seconds=defaults["min_interval"],
                hour_reset_at=datetime.utcnow() + timedelta(hours=1),
                day_reset_at=datetime.utcnow().replace(hour=0, minute=0, second=0) + timedelta(days=1)
            )
            db.add(rate_limit)
            await db.commit()
            await db.refresh(rate_limit)
            logger.info(f"📝 Created rate limit for {device_id}/{channel}")

        return rate_limit

    async def check_rate_limit(
        self,
        db: AsyncSession,
        device_id: str,
        channel: str
    ) -> Tuple[bool, Optional[str], Optional[int]]:
        """
        Check if action is allowed under rate limits.

        Args:
            db: Database session
            device_id: Device identifier
            channel: Channel type

        Returns:
            Tuple of (allowed: bool, reason: str|None, wait_seconds: int|None)
        """
        rate_limit = await self.get_or_create_limit(db, device_id, channel)
        now = datetime.utcnow()

        # Reset counters if needed
        if rate_limit.hour_reset_at and now >= rate_limit.hour_reset_at:
            rate_limit.current_hour_count = 0
            rate_limit.hour_reset_at = now + timedelta(hours=1)

        if rate_limit.day_reset_at and now >= rate_limit.day_reset_at:
            rate_limit.current_day_count = 0
            rate_limit.day_reset_at = now.replace(hour=0, minute=0, second=0) + timedelta(days=1)

        # Check if blocked
        if rate_limit.is_blocked:
            if rate_limit.blocked_until and now < rate_limit.blocked_until:
                wait_seconds = int((rate_limit.blocked_until - now).total_seconds())
                return False, f"Blocked: {rate_limit.block_reason}", wait_seconds
            else:
                # Unblock
                rate_limit.is_blocked = False
                rate_limit.blocked_until = None
                rate_limit.block_reason = None

        # Check hourly limit
        if rate_limit.current_hour_count >= rate_limit.max_per_hour:
            wait_seconds = int((rate_limit.hour_reset_at - now).total_seconds()) if rate_limit.hour_reset_at else 3600
            return False, f"Hourly limit reached ({rate_limit.max_per_hour}/hr)", wait_seconds

        # Check daily limit
        if rate_limit.current_day_count >= rate_limit.max_per_day:
            wait_seconds = int((rate_limit.day_reset_at - now).total_seconds()) if rate_limit.day_reset_at else 86400
            return False, f"Daily limit reached ({rate_limit.max_per_day}/day)", wait_seconds

        # Check minimum interval
        if rate_limit.last_action_at:
            elapsed = (now - rate_limit.last_action_at).total_seconds()
            if elapsed < rate_limit.min_interval_seconds:
                wait_seconds = int(rate_limit.min_interval_seconds - elapsed)
                return False, f"Minimum interval not met ({rate_limit.min_interval_seconds}s)", wait_seconds

        await db.commit()
        return True, None, None

    async def record_action(
        self,
        db: AsyncSession,
        device_id: str,
        channel: str,
        success: bool = True
    ) -> None:
        """
        Record an action for rate limiting.

        Args:
            db: Database session
            device_id: Device identifier
            channel: Channel type
            success: Whether the action was successful
        """
        rate_limit = await self.get_or_create_limit(db, device_id, channel)

        rate_limit.current_hour_count += 1
        rate_limit.current_day_count += 1
        rate_limit.last_action_at = datetime.utcnow()

        await db.commit()

        logger.debug(
            f"⏱️ Rate limit updated: {device_id}/{channel} "
            f"({rate_limit.current_hour_count}/{rate_limit.max_per_hour}/hr, "
            f"{rate_limit.current_day_count}/{rate_limit.max_per_day}/day)"
        )

    async def block_device(
        self,
        db: AsyncSession,
        device_id: str,
        channel: str,
        duration_minutes: int,
        reason: str
    ) -> None:
        """
        Temporarily block a device+channel.

        Args:
            db: Database session
            device_id: Device identifier
            channel: Channel type
            duration_minutes: Block duration in minutes
            reason: Reason for blocking
        """
        rate_limit = await self.get_or_create_limit(db, device_id, channel)

        rate_limit.is_blocked = True
        rate_limit.blocked_until = datetime.utcnow() + timedelta(minutes=duration_minutes)
        rate_limit.block_reason = reason

        await db.commit()
        logger.warning(f"🚫 Blocked {device_id}/{channel} for {duration_minutes}min: {reason}")

    async def unblock_device(
        self,
        db: AsyncSession,
        device_id: str,
        channel: str
    ) -> None:
        """
        Unblock a device+channel.

        Args:
            db: Database session
            device_id: Device identifier
            channel: Channel type
        """
        rate_limit = await self.get_or_create_limit(db, device_id, channel)

        rate_limit.is_blocked = False
        rate_limit.blocked_until = None
        rate_limit.block_reason = None

        await db.commit()
        logger.info(f"✅ Unblocked {device_id}/{channel}")

    async def get_status(
        self,
        db: AsyncSession,
        device_id: str,
        channel: Optional[str] = None
    ) -> Dict:
        """
        Get rate limit status for device.

        Args:
            db: Database session
            device_id: Device identifier
            channel: Optional specific channel (returns all if None)

        Returns:
            Dictionary with rate limit status
        """
        if channel:
            rate_limit = await self.get_or_create_limit(db, device_id, channel)
            return self._format_status(rate_limit)

        # Get all channels for device
        result = await db.execute(
            select(RateLimit).where(RateLimit.device_id == device_id)
        )
        rate_limits = result.scalars().all()

        return {
            "device_id": device_id,
            "channels": {rl.limit_type: self._format_status(rl) for rl in rate_limits}
        }

    def _format_status(self, rate_limit: RateLimit) -> Dict:
        """Format rate limit status for API response"""
        now = datetime.utcnow()

        return {
            "channel": rate_limit.limit_type,
            "hourly": {
                "current": rate_limit.current_hour_count,
                "max": rate_limit.max_per_hour,
                "remaining": max(0, rate_limit.max_per_hour - rate_limit.current_hour_count),
                "resets_at": rate_limit.hour_reset_at.isoformat() if rate_limit.hour_reset_at else None
            },
            "daily": {
                "current": rate_limit.current_day_count,
                "max": rate_limit.max_per_day,
                "remaining": max(0, rate_limit.max_per_day - rate_limit.current_day_count),
                "resets_at": rate_limit.day_reset_at.isoformat() if rate_limit.day_reset_at else None
            },
            "min_interval_seconds": rate_limit.min_interval_seconds,
            "last_action_at": rate_limit.last_action_at.isoformat() if rate_limit.last_action_at else None,
            "is_blocked": rate_limit.is_blocked,
            "blocked_until": rate_limit.blocked_until.isoformat() if rate_limit.blocked_until else None,
            "block_reason": rate_limit.block_reason
        }

    async def wait_for_slot(
        self,
        db: AsyncSession,
        device_id: str,
        channel: str,
        max_wait_seconds: int = 300
    ) -> bool:
        """
        Wait until rate limit allows action.

        Args:
            db: Database session
            device_id: Device identifier
            channel: Channel type
            max_wait_seconds: Maximum time to wait

        Returns:
            True if slot became available, False if timed out
        """
        start_time = datetime.utcnow()

        while True:
            allowed, reason, wait_seconds = await self.check_rate_limit(db, device_id, channel)

            if allowed:
                return True

            elapsed = (datetime.utcnow() - start_time).total_seconds()

            if elapsed >= max_wait_seconds:
                logger.warning(f"⏰ Rate limit wait timeout for {device_id}/{channel}: {reason}")
                return False

            # Wait for the recommended time (capped)
            wait = min(wait_seconds or 30, max_wait_seconds - elapsed)
            logger.debug(f"⏳ Waiting {wait}s for rate limit: {reason}")
            await asyncio.sleep(wait)


# Global instance
rate_limit_service = RateLimitService()
