"""Screenshot Service - manages screenshot capture, storage, and cleanup"""

import asyncio
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from loguru import logger


class ScreenshotService:
    """Manages screenshot capture, organization, and cleanup for automation tasks"""

    def __init__(
        self,
        base_dir: str = "data/screenshots",
        retention_days: int = 7,
        max_storage_mb: int = 1000
    ):
        """
        Initialize screenshot service.

        Args:
            base_dir: Base directory for storing screenshots
            retention_days: Days to keep screenshots before cleanup
            max_storage_mb: Maximum storage in MB before forced cleanup
        """
        self.base_dir = Path(base_dir)
        self.retention_days = retention_days
        self.max_storage_mb = max_storage_mb

        # Create base directory if not exists
        self.base_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"📸 Screenshot service initialized: {self.base_dir}")

    def get_screenshot_path(
        self,
        device_id: str,
        task_id: Optional[str] = None,
        step_name: Optional[str] = None,
        suffix: str = ""
    ) -> Path:
        """
        Generate organized screenshot path.

        Structure: screenshots/{date}/{device_id}/{task_id}_{step}_{timestamp}{suffix}.png

        Args:
            device_id: Device identifier
            task_id: Optional task ID
            step_name: Optional step name (e.g., "before_send", "after_send")
            suffix: Optional suffix for filename

        Returns:
            Path object for the screenshot
        """
        date_str = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%H%M%S")

        # Build directory path
        dir_path = self.base_dir / date_str / device_id
        dir_path.mkdir(parents=True, exist_ok=True)

        # Build filename
        parts = []
        if task_id:
            parts.append(task_id[:8])  # First 8 chars of task_id
        if step_name:
            parts.append(step_name)
        parts.append(timestamp)
        if suffix:
            parts.append(suffix)

        filename = "_".join(parts) + ".png"

        return dir_path / filename

    async def save_screenshot(
        self,
        image_data: bytes,
        device_id: str,
        task_id: Optional[str] = None,
        step_name: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Optional[str]:
        """
        Save screenshot with metadata.

        Args:
            image_data: Raw PNG image bytes
            device_id: Device identifier
            task_id: Optional task ID
            step_name: Optional step name
            metadata: Optional metadata to save alongside

        Returns:
            Path to saved screenshot or None on error
        """
        try:
            path = self.get_screenshot_path(device_id, task_id, step_name)

            # Save image
            path.write_bytes(image_data)

            # Save metadata if provided
            if metadata:
                meta_path = path.with_suffix(".json")
                import json
                meta_path.write_text(json.dumps(metadata, indent=2, default=str))

            logger.debug(f"📸 Saved screenshot: {path}")
            return str(path)

        except Exception as e:
            logger.error(f"❌ Failed to save screenshot: {e}")
            return None

    async def capture_from_device(
        self,
        device,
        task_id: Optional[str] = None,
        step_name: Optional[str] = None
    ) -> Optional[str]:
        """
        Capture screenshot directly from device.

        Args:
            device: Device object with screenshot capability
            task_id: Optional task ID
            step_name: Optional step name

        Returns:
            Path to saved screenshot or None on error
        """
        try:
            # Get screenshot from device (assumes device has take_screenshot method)
            if hasattr(device, 'take_screenshot'):
                image_data = await device.take_screenshot()
                if image_data:
                    return await self.save_screenshot(
                        image_data,
                        device.device_id,
                        task_id,
                        step_name,
                        metadata={
                            "captured_at": datetime.now().isoformat(),
                            "device_id": device.device_id,
                            "task_id": task_id,
                            "step_name": step_name
                        }
                    )

            logger.warning(f"⚠️ Device {device.device_id} has no screenshot capability")
            return None

        except Exception as e:
            logger.error(f"❌ Failed to capture screenshot from device: {e}")
            return None

    def get_screenshots_for_task(self, task_id: str) -> List[Path]:
        """
        Get all screenshots for a specific task.

        Args:
            task_id: Task identifier

        Returns:
            List of screenshot paths
        """
        screenshots = []
        task_prefix = task_id[:8]

        for date_dir in self.base_dir.iterdir():
            if not date_dir.is_dir():
                continue
            for device_dir in date_dir.iterdir():
                if not device_dir.is_dir():
                    continue
                for screenshot in device_dir.glob(f"{task_prefix}*.png"):
                    screenshots.append(screenshot)

        return sorted(screenshots, key=lambda p: p.stat().st_mtime)

    def get_screenshots_for_device(
        self,
        device_id: str,
        date: Optional[datetime] = None
    ) -> List[Path]:
        """
        Get all screenshots for a specific device.

        Args:
            device_id: Device identifier
            date: Optional specific date (defaults to today)

        Returns:
            List of screenshot paths
        """
        if date is None:
            date = datetime.now()

        date_str = date.strftime("%Y-%m-%d")
        device_dir = self.base_dir / date_str / device_id

        if not device_dir.exists():
            return []

        return sorted(device_dir.glob("*.png"), key=lambda p: p.stat().st_mtime)

    async def cleanup_old_screenshots(self) -> Tuple[int, int]:
        """
        Remove screenshots older than retention period.

        Returns:
            Tuple of (files_deleted, bytes_freed)
        """
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        files_deleted = 0
        bytes_freed = 0

        try:
            for date_dir in self.base_dir.iterdir():
                if not date_dir.is_dir():
                    continue

                # Parse date from directory name
                try:
                    dir_date = datetime.strptime(date_dir.name, "%Y-%m-%d")
                except ValueError:
                    continue

                # Remove old directories
                if dir_date < cutoff_date:
                    for f in date_dir.rglob("*"):
                        if f.is_file():
                            bytes_freed += f.stat().st_size
                            files_deleted += 1

                    shutil.rmtree(date_dir)
                    logger.info(f"🗑️ Removed old screenshot directory: {date_dir.name}")

            logger.info(f"🗑️ Cleanup complete: {files_deleted} files, {bytes_freed / 1024 / 1024:.1f} MB freed")
            return files_deleted, bytes_freed

        except Exception as e:
            logger.error(f"❌ Cleanup error: {e}")
            return files_deleted, bytes_freed

    def get_storage_stats(self) -> Dict:
        """
        Get storage statistics.

        Returns:
            Dictionary with storage stats
        """
        total_size = 0
        total_files = 0
        by_date: Dict[str, int] = {}
        by_device: Dict[str, int] = {}

        for date_dir in self.base_dir.iterdir():
            if not date_dir.is_dir():
                continue

            date_size = 0
            for device_dir in date_dir.iterdir():
                if not device_dir.is_dir():
                    continue

                device_size = 0
                for f in device_dir.glob("*.png"):
                    size = f.stat().st_size
                    device_size += size
                    total_files += 1

                by_device[device_dir.name] = by_device.get(device_dir.name, 0) + device_size
                date_size += device_size

            by_date[date_dir.name] = date_size
            total_size += date_size

        return {
            "total_size_mb": total_size / 1024 / 1024,
            "total_files": total_files,
            "retention_days": self.retention_days,
            "max_storage_mb": self.max_storage_mb,
            "by_date": {k: v / 1024 / 1024 for k, v in by_date.items()},
            "by_device": {k: v / 1024 / 1024 for k, v in by_device.items()}
        }

    async def check_storage_limit(self) -> bool:
        """
        Check if storage limit is exceeded and trigger cleanup if needed.

        Returns:
            True if cleanup was triggered
        """
        stats = self.get_storage_stats()

        if stats["total_size_mb"] > self.max_storage_mb:
            logger.warning(f"⚠️ Storage limit exceeded: {stats['total_size_mb']:.1f}MB / {self.max_storage_mb}MB")
            await self.cleanup_old_screenshots()
            return True

        return False


# Global instance
screenshot_service = ScreenshotService()
