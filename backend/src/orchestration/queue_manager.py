"""
Queue Manager - Priority-based task queue with async processing

Features:
- Priority queue with configurable priorities (1-10)
- Rate limiting per device
- Exponential backoff on failures
- WebSocket integration for real-time updates
- Graceful shutdown handling
"""

import asyncio
import heapq
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Awaitable
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger


class QueueItemStatus(str, Enum):
    """Status of a queued item"""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


@dataclass(order=True)
class QueueItem:
    """
    Represents an item in the priority queue.
    Lower priority number = higher priority (1 is highest).
    """
    # Priority for heap ordering (inverted: 10-priority so 10 becomes highest)
    sort_priority: int = field(compare=True)

    # Actual item data (not used for comparison)
    id: str = field(compare=False)
    item_type: str = field(compare=False)  # 'scenario' or 'task'
    reference_id: str = field(compare=False)  # scenario_id or task_id
    device_id: Optional[str] = field(compare=False, default=None)
    priority: int = field(compare=False, default=5)

    # Execution state
    status: QueueItemStatus = field(compare=False, default=QueueItemStatus.QUEUED)
    attempt_count: int = field(compare=False, default=0)
    max_attempts: int = field(compare=False, default=3)

    # Timestamps
    queued_at: datetime = field(compare=False, default_factory=datetime.utcnow)
    started_at: Optional[datetime] = field(compare=False, default=None)
    completed_at: Optional[datetime] = field(compare=False, default=None)
    next_retry_at: Optional[datetime] = field(compare=False, default=None)

    # Callback for execution
    callback: Optional[Callable[..., Awaitable[Any]]] = field(compare=False, default=None)
    callback_args: tuple = field(compare=False, default_factory=tuple)
    callback_kwargs: Dict[str, Any] = field(compare=False, default_factory=dict)

    # Result/Error
    result: Optional[Any] = field(compare=False, default=None)
    error_message: Optional[str] = field(compare=False, default=None)


class QueueManager:
    """
    Priority-based task queue manager.

    Handles:
    - Priority ordering (1-10, where 10 is highest priority)
    - Per-device rate limiting
    - Exponential backoff on failures
    - Concurrent processing with worker limit
    - WebSocket notifications
    """

    def __init__(
        self,
        max_workers: int = 4,
        default_rate_limit_seconds: float = 30.0,
        max_retry_delay_seconds: float = 3600.0,
        base_retry_delay_seconds: float = 60.0
    ):
        """
        Initialize Queue Manager.

        Args:
            max_workers: Maximum concurrent workers processing queue items
            default_rate_limit_seconds: Default time between tasks on same device
            max_retry_delay_seconds: Maximum delay for exponential backoff (1 hour)
            base_retry_delay_seconds: Base delay for retry calculation
        """
        self.max_workers = max_workers
        self.default_rate_limit = default_rate_limit_seconds
        self.max_retry_delay = max_retry_delay_seconds
        self.base_retry_delay = base_retry_delay_seconds

        # Priority queue (heap)
        self._queue: List[QueueItem] = []

        # Active processing items by ID
        self._processing: Dict[str, QueueItem] = {}

        # Items waiting for retry
        self._retry_queue: Dict[str, QueueItem] = {}

        # Rate limiting: device_id -> last_action_time
        self._device_last_action: Dict[str, datetime] = {}

        # Per-device rate limits (can be customized)
        self._device_rate_limits: Dict[str, float] = {}

        # Worker control
        self._running = False
        self._workers: List[asyncio.Task] = []
        self._queue_lock = asyncio.Lock()

        # Statistics
        self._stats = {
            "total_queued": 0,
            "total_completed": 0,
            "total_failed": 0,
            "total_retried": 0,
        }

        # WebSocket manager reference (set during initialization)
        self._ws_manager = None

        logger.info(f"QueueManager initialized (workers: {max_workers}, rate_limit: {default_rate_limit_seconds}s)")

    def set_websocket_manager(self, ws_manager) -> None:
        """Set WebSocket manager for real-time updates"""
        self._ws_manager = ws_manager

    async def start(self) -> None:
        """Start the queue manager workers"""
        if self._running:
            logger.warning("QueueManager is already running")
            return

        self._running = True
        logger.info(f"Starting QueueManager with {self.max_workers} workers...")

        # Start worker tasks
        for i in range(self.max_workers):
            worker = asyncio.create_task(self._worker(i))
            self._workers.append(worker)

        # Start retry checker
        self._workers.append(asyncio.create_task(self._retry_checker()))

        logger.success("QueueManager started successfully")

    async def stop(self, timeout: float = 30.0) -> None:
        """
        Stop the queue manager gracefully.

        Args:
            timeout: Maximum time to wait for workers to finish
        """
        if not self._running:
            return

        logger.info("Stopping QueueManager...")
        self._running = False

        # Wait for workers to finish (with timeout)
        if self._workers:
            try:
                await asyncio.wait_for(
                    asyncio.gather(*self._workers, return_exceptions=True),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                logger.warning(f"QueueManager workers didn't finish within {timeout}s, cancelling...")
                for worker in self._workers:
                    worker.cancel()

        self._workers.clear()
        logger.success("QueueManager stopped")

    async def enqueue(
        self,
        item_type: str,
        reference_id: str,
        callback: Callable[..., Awaitable[Any]],
        device_id: Optional[str] = None,
        priority: int = 5,
        max_attempts: int = 3,
        callback_args: tuple = (),
        callback_kwargs: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Add an item to the queue.

        Args:
            item_type: Type of item ('scenario' or 'task')
            reference_id: ID of the scenario or task
            callback: Async function to execute
            device_id: Target device ID (for rate limiting)
            priority: Priority 1-10 (10 is highest)
            max_attempts: Maximum retry attempts
            callback_args: Arguments for callback
            callback_kwargs: Keyword arguments for callback

        Returns:
            str: Queue item ID
        """
        import uuid

        item_id = str(uuid.uuid4())

        # Invert priority for heap (lower number = higher priority in heap)
        sort_priority = 11 - priority  # 10 becomes 1, 1 becomes 10

        item = QueueItem(
            sort_priority=sort_priority,
            id=item_id,
            item_type=item_type,
            reference_id=reference_id,
            device_id=device_id,
            priority=priority,
            max_attempts=max_attempts,
            callback=callback,
            callback_args=callback_args,
            callback_kwargs=callback_kwargs or {},
        )

        async with self._queue_lock:
            heapq.heappush(self._queue, item)
            self._stats["total_queued"] += 1

        logger.info(f"Enqueued {item_type} {reference_id} (priority: {priority}, id: {item_id})")

        # Notify via WebSocket
        await self._notify_queue_update("item_queued", item)

        return item_id

    async def cancel(self, item_id: str) -> bool:
        """
        Cancel a queued item.

        Args:
            item_id: Queue item ID to cancel

        Returns:
            bool: True if cancelled, False if not found or already processing
        """
        async with self._queue_lock:
            # Check if in queue
            for i, item in enumerate(self._queue):
                if item.id == item_id:
                    item.status = QueueItemStatus.CANCELLED
                    self._queue.pop(i)
                    heapq.heapify(self._queue)
                    logger.info(f"Cancelled queued item: {item_id}")
                    await self._notify_queue_update("item_cancelled", item)
                    return True

            # Check retry queue
            if item_id in self._retry_queue:
                item = self._retry_queue.pop(item_id)
                item.status = QueueItemStatus.CANCELLED
                logger.info(f"Cancelled retry item: {item_id}")
                await self._notify_queue_update("item_cancelled", item)
                return True

        logger.warning(f"Item not found for cancellation: {item_id}")
        return False

    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status"""
        return {
            "queued_count": len(self._queue),
            "processing_count": len(self._processing),
            "retry_count": len(self._retry_queue),
            "workers": self.max_workers,
            "is_running": self._running,
            "stats": self._stats.copy(),
        }

    def get_queued_items(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get list of queued items"""
        items = []
        for item in sorted(self._queue)[:limit]:
            items.append({
                "id": item.id,
                "type": item.item_type,
                "reference_id": item.reference_id,
                "device_id": item.device_id,
                "priority": item.priority,
                "status": item.status.value,
                "queued_at": item.queued_at.isoformat(),
            })
        return items

    def set_device_rate_limit(self, device_id: str, seconds: float) -> None:
        """Set custom rate limit for a specific device"""
        self._device_rate_limits[device_id] = seconds
        logger.debug(f"Set rate limit for {device_id}: {seconds}s")

    async def _worker(self, worker_id: int) -> None:
        """
        Worker coroutine that processes queue items.

        Args:
            worker_id: Worker identifier for logging
        """
        logger.debug(f"Worker {worker_id} started")

        while self._running:
            item = await self._get_next_item()

            if item is None:
                # No item available, wait a bit
                await asyncio.sleep(1.0)
                continue

            # Process the item
            await self._process_item(item, worker_id)

        logger.debug(f"Worker {worker_id} stopped")

    async def _get_next_item(self) -> Optional[QueueItem]:
        """Get next item from queue that's ready to process"""
        async with self._queue_lock:
            if not self._queue:
                return None

            # Check each item for rate limiting
            for i, item in enumerate(sorted(self._queue)):
                if self._can_process_on_device(item.device_id):
                    # Remove from queue
                    self._queue.remove(item)
                    heapq.heapify(self._queue)

                    # Add to processing
                    item.status = QueueItemStatus.PROCESSING
                    item.started_at = datetime.utcnow()
                    self._processing[item.id] = item

                    return item

        return None

    def _can_process_on_device(self, device_id: Optional[str]) -> bool:
        """Check if we can process on the given device (rate limiting)"""
        if device_id is None:
            return True

        last_action = self._device_last_action.get(device_id)
        if last_action is None:
            return True

        rate_limit = self._device_rate_limits.get(device_id, self.default_rate_limit)
        time_since_last = (datetime.utcnow() - last_action).total_seconds()

        return time_since_last >= rate_limit

    async def _process_item(self, item: QueueItem, worker_id: int) -> None:
        """Process a single queue item"""
        logger.info(f"Worker {worker_id} processing {item.item_type} {item.reference_id}")

        try:
            # Update device last action time
            if item.device_id:
                self._device_last_action[item.device_id] = datetime.utcnow()

            # Execute callback
            if item.callback:
                result = await item.callback(*item.callback_args, **item.callback_kwargs)
                item.result = result

            # Success
            item.status = QueueItemStatus.COMPLETED
            item.completed_at = datetime.utcnow()
            self._stats["total_completed"] += 1

            logger.success(f"Completed {item.item_type} {item.reference_id}")
            await self._notify_queue_update("item_completed", item)

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed {item.item_type} {item.reference_id}: {error_msg}")

            item.error_message = error_msg
            item.attempt_count += 1

            # Check if we should retry
            if item.attempt_count < item.max_attempts:
                await self._schedule_retry(item)
            else:
                item.status = QueueItemStatus.FAILED
                item.completed_at = datetime.utcnow()
                self._stats["total_failed"] += 1
                await self._notify_queue_update("item_failed", item)

        finally:
            # Remove from processing
            self._processing.pop(item.id, None)

    async def _schedule_retry(self, item: QueueItem) -> None:
        """Schedule an item for retry with exponential backoff"""
        # Calculate delay: base * 2^(attempt-1), capped at max
        delay_seconds = min(
            self.base_retry_delay * (2 ** (item.attempt_count - 1)),
            self.max_retry_delay
        )

        item.status = QueueItemStatus.RETRYING
        item.next_retry_at = datetime.utcnow() + timedelta(seconds=delay_seconds)

        self._retry_queue[item.id] = item
        self._stats["total_retried"] += 1

        logger.info(
            f"Scheduled retry for {item.item_type} {item.reference_id} "
            f"(attempt {item.attempt_count}/{item.max_attempts}, delay: {delay_seconds}s)"
        )

        await self._notify_queue_update("item_retrying", item)

    async def _retry_checker(self) -> None:
        """Background task to move items from retry queue back to main queue"""
        logger.debug("Retry checker started")

        while self._running:
            now = datetime.utcnow()
            items_to_retry = []

            # Find items ready for retry
            for item_id, item in list(self._retry_queue.items()):
                if item.next_retry_at and item.next_retry_at <= now:
                    items_to_retry.append(item_id)

            # Move items back to queue
            for item_id in items_to_retry:
                item = self._retry_queue.pop(item_id)
                item.status = QueueItemStatus.QUEUED
                item.next_retry_at = None

                async with self._queue_lock:
                    heapq.heappush(self._queue, item)

                logger.info(f"Retrying {item.item_type} {item.reference_id}")

            await asyncio.sleep(5.0)  # Check every 5 seconds

        logger.debug("Retry checker stopped")

    async def _notify_queue_update(self, event_type: str, item: QueueItem) -> None:
        """Send WebSocket notification about queue update"""
        if not self._ws_manager:
            return

        try:
            await self._ws_manager.broadcast({
                "type": f"queue_{event_type}",
                "data": {
                    "id": item.id,
                    "item_type": item.item_type,
                    "reference_id": item.reference_id,
                    "status": item.status.value,
                    "priority": item.priority,
                    "attempt_count": item.attempt_count,
                    "error_message": item.error_message,
                }
            })
        except Exception as e:
            logger.error(f"Failed to send WebSocket notification: {e}")


# Global instance
queue_manager = QueueManager()
