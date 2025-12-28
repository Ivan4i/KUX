"""
Task Scheduler - CRON-like job scheduling for scenarios and tasks

Features:
- CRON expression support (via croniter)
- One-time scheduled execution
- Recurring jobs with configurable repeat counts
- Database persistence for jobs
- Integration with QueueManager
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Awaitable
from dataclasses import dataclass, field
from loguru import logger

# croniter is optional - fallback to basic scheduling if not available
try:
    from croniter import croniter
    HAS_CRONITER = True
except ImportError:
    HAS_CRONITER = False
    logger.warning("croniter not installed. CRON expressions will not work. Install with: pip install croniter")


@dataclass
class ScheduledJob:
    """Represents a scheduled job"""
    id: str
    job_type: str  # 'scenario', 'task', 'maintenance'
    reference_id: Optional[str]  # scenario_id or task_id

    # Scheduling
    cron_expression: Optional[str] = None
    scheduled_at: Optional[datetime] = None  # For one-time execution
    repeat_count: int = 0  # 0 = unlimited

    # State
    is_active: bool = True
    run_count: int = 0
    last_run_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None

    # Callback
    callback: Optional[Callable[..., Awaitable[Any]]] = None
    callback_args: tuple = field(default_factory=tuple)
    callback_kwargs: Dict[str, Any] = field(default_factory=dict)

    # Config
    config: Optional[Dict[str, Any]] = None

    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


class TaskScheduler:
    """
    CRON-like task scheduler.

    Supports:
    - CRON expressions: "0 9 * * *" (daily at 9am)
    - One-time scheduling: scheduled_at datetime
    - Recurring jobs with repeat limits
    - Database persistence
    """

    def __init__(
        self,
        check_interval_seconds: float = 10.0,
        timezone: str = "UTC"
    ):
        """
        Initialize Task Scheduler.

        Args:
            check_interval_seconds: How often to check for due jobs
            timezone: Default timezone for scheduling
        """
        self.check_interval = check_interval_seconds
        self.timezone = timezone

        # Active scheduled jobs
        self._jobs: Dict[str, ScheduledJob] = {}

        # Control
        self._running = False
        self._scheduler_task: Optional[asyncio.Task] = None
        self._lock = asyncio.Lock()

        # Queue manager reference
        self._queue_manager = None

        # WebSocket manager reference
        self._ws_manager = None

        # Database session factory (set during initialization)
        self._get_db = None

        logger.info(f"TaskScheduler initialized (check_interval: {check_interval_seconds}s)")

    def set_queue_manager(self, queue_manager) -> None:
        """Set queue manager for job execution"""
        self._queue_manager = queue_manager

    def set_websocket_manager(self, ws_manager) -> None:
        """Set WebSocket manager for real-time updates"""
        self._ws_manager = ws_manager

    def set_db_factory(self, get_db: Callable) -> None:
        """Set database session factory"""
        self._get_db = get_db

    async def start(self) -> None:
        """Start the scheduler"""
        if self._running:
            logger.warning("TaskScheduler is already running")
            return

        self._running = True
        self._scheduler_task = asyncio.create_task(self._scheduler_loop())

        logger.success("TaskScheduler started")

    async def stop(self) -> None:
        """Stop the scheduler"""
        if not self._running:
            return

        logger.info("Stopping TaskScheduler...")
        self._running = False

        if self._scheduler_task:
            self._scheduler_task.cancel()
            try:
                await self._scheduler_task
            except asyncio.CancelledError:
                pass

        logger.success("TaskScheduler stopped")

    async def add_job(
        self,
        job_id: str,
        job_type: str,
        reference_id: Optional[str] = None,
        cron_expression: Optional[str] = None,
        scheduled_at: Optional[datetime] = None,
        repeat_count: int = 0,
        callback: Optional[Callable[..., Awaitable[Any]]] = None,
        callback_args: tuple = (),
        callback_kwargs: Optional[Dict[str, Any]] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> ScheduledJob:
        """
        Add a scheduled job.

        Args:
            job_id: Unique job identifier
            job_type: Type of job ('scenario', 'task', 'maintenance')
            reference_id: ID of the scenario or task
            cron_expression: CRON expression for recurring jobs
            scheduled_at: One-time execution datetime
            repeat_count: Number of times to repeat (0 = unlimited for cron)
            callback: Async function to execute
            callback_args: Arguments for callback
            callback_kwargs: Keyword arguments for callback
            config: Additional configuration

        Returns:
            ScheduledJob: The created job
        """
        # Validate CRON expression
        if cron_expression and HAS_CRONITER:
            try:
                croniter(cron_expression)
            except Exception as e:
                raise ValueError(f"Invalid CRON expression: {cron_expression}. Error: {e}")

        job = ScheduledJob(
            id=job_id,
            job_type=job_type,
            reference_id=reference_id,
            cron_expression=cron_expression,
            scheduled_at=scheduled_at,
            repeat_count=repeat_count,
            callback=callback,
            callback_args=callback_args,
            callback_kwargs=callback_kwargs or {},
            config=config,
        )

        # Calculate next run time
        job.next_run_at = self._calculate_next_run(job)

        async with self._lock:
            self._jobs[job_id] = job

        logger.info(
            f"Added scheduled job: {job_id} ({job_type}), "
            f"next_run: {job.next_run_at}"
        )

        await self._notify_job_update("job_added", job)

        return job

    async def remove_job(self, job_id: str) -> bool:
        """
        Remove a scheduled job.

        Args:
            job_id: Job ID to remove

        Returns:
            bool: True if removed, False if not found
        """
        async with self._lock:
            if job_id in self._jobs:
                job = self._jobs.pop(job_id)
                logger.info(f"Removed scheduled job: {job_id}")
                await self._notify_job_update("job_removed", job)
                return True

        logger.warning(f"Job not found: {job_id}")
        return False

    async def pause_job(self, job_id: str) -> bool:
        """Pause a scheduled job"""
        async with self._lock:
            if job_id in self._jobs:
                self._jobs[job_id].is_active = False
                self._jobs[job_id].updated_at = datetime.utcnow()
                logger.info(f"Paused scheduled job: {job_id}")
                await self._notify_job_update("job_paused", self._jobs[job_id])
                return True
        return False

    async def resume_job(self, job_id: str) -> bool:
        """Resume a paused job"""
        async with self._lock:
            if job_id in self._jobs:
                job = self._jobs[job_id]
                job.is_active = True
                job.next_run_at = self._calculate_next_run(job)
                job.updated_at = datetime.utcnow()
                logger.info(f"Resumed scheduled job: {job_id}")
                await self._notify_job_update("job_resumed", job)
                return True
        return False

    def get_job(self, job_id: str) -> Optional[ScheduledJob]:
        """Get a scheduled job by ID"""
        return self._jobs.get(job_id)

    def get_all_jobs(self) -> List[ScheduledJob]:
        """Get all scheduled jobs"""
        return list(self._jobs.values())

    def get_status(self) -> Dict[str, Any]:
        """Get scheduler status"""
        active_jobs = [j for j in self._jobs.values() if j.is_active]
        upcoming = sorted(
            [j for j in active_jobs if j.next_run_at],
            key=lambda x: x.next_run_at
        )

        return {
            "is_running": self._running,
            "total_jobs": len(self._jobs),
            "active_jobs": len(active_jobs),
            "check_interval": self.check_interval,
            "next_job": {
                "id": upcoming[0].id,
                "type": upcoming[0].job_type,
                "next_run": upcoming[0].next_run_at.isoformat() if upcoming[0].next_run_at else None,
            } if upcoming else None,
        }

    def _calculate_next_run(self, job: ScheduledJob) -> Optional[datetime]:
        """Calculate next run time for a job"""
        now = datetime.utcnow()

        # Check if job should stop (repeat limit reached)
        if job.repeat_count > 0 and job.run_count >= job.repeat_count:
            return None

        # One-time scheduled execution
        if job.scheduled_at:
            if job.run_count == 0 and job.scheduled_at > now:
                return job.scheduled_at
            return None

        # CRON expression
        if job.cron_expression and HAS_CRONITER:
            try:
                cron = croniter(job.cron_expression, now)
                return cron.get_next(datetime)
            except Exception as e:
                logger.error(f"Error calculating next run for job {job.id}: {e}")
                return None

        return None

    async def _scheduler_loop(self) -> None:
        """Main scheduler loop"""
        logger.debug("Scheduler loop started")

        while self._running:
            try:
                await self._check_and_execute_jobs()
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")

            await asyncio.sleep(self.check_interval)

        logger.debug("Scheduler loop stopped")

    async def _check_and_execute_jobs(self) -> None:
        """Check for due jobs and execute them"""
        now = datetime.utcnow()
        jobs_to_run = []

        async with self._lock:
            for job in self._jobs.values():
                if not job.is_active:
                    continue

                if job.next_run_at and job.next_run_at <= now:
                    jobs_to_run.append(job)

        # Execute due jobs
        for job in jobs_to_run:
            await self._execute_job(job)

    async def _execute_job(self, job: ScheduledJob) -> None:
        """Execute a scheduled job"""
        logger.info(f"Executing scheduled job: {job.id} ({job.job_type})")

        try:
            # Update job state
            job.last_run_at = datetime.utcnow()
            job.run_count += 1

            # If we have a queue manager, enqueue the job
            if self._queue_manager and job.reference_id:
                await self._queue_manager.enqueue(
                    item_type=job.job_type,
                    reference_id=job.reference_id,
                    callback=job.callback,
                    callback_args=job.callback_args,
                    callback_kwargs=job.callback_kwargs,
                    priority=job.config.get("priority", 5) if job.config else 5,
                )
            # Otherwise execute directly
            elif job.callback:
                await job.callback(*job.callback_args, **job.callback_kwargs)

            # Calculate next run
            job.next_run_at = self._calculate_next_run(job)
            job.updated_at = datetime.utcnow()

            # Deactivate if no more runs scheduled
            if job.next_run_at is None:
                job.is_active = False
                logger.info(f"Job {job.id} completed all scheduled runs")

            await self._notify_job_update("job_executed", job)

        except Exception as e:
            logger.error(f"Error executing job {job.id}: {e}")
            await self._notify_job_update("job_error", job, error=str(e))

    async def _notify_job_update(
        self,
        event_type: str,
        job: ScheduledJob,
        error: Optional[str] = None
    ) -> None:
        """Send WebSocket notification about job update"""
        if not self._ws_manager:
            return

        try:
            data = {
                "id": job.id,
                "job_type": job.job_type,
                "reference_id": job.reference_id,
                "is_active": job.is_active,
                "run_count": job.run_count,
                "last_run_at": job.last_run_at.isoformat() if job.last_run_at else None,
                "next_run_at": job.next_run_at.isoformat() if job.next_run_at else None,
            }

            if error:
                data["error"] = error

            await self._ws_manager.broadcast({
                "type": f"scheduler_{event_type}",
                "data": data,
            })
        except Exception as e:
            logger.error(f"Failed to send scheduler notification: {e}")

    async def load_from_database(self) -> int:
        """
        Load scheduled jobs from database.

        Returns:
            int: Number of jobs loaded
        """
        if not self._get_db:
            logger.warning("Database not configured, skipping job load")
            return 0

        try:
            from ..database.db import SessionLocal
            from ..database import models

            db = SessionLocal()
            try:
                # Load active scheduled jobs
                db_jobs = db.query(models.ScheduledJob).filter(
                    models.ScheduledJob.is_active == True
                ).all()

                for db_job in db_jobs:
                    job = ScheduledJob(
                        id=db_job.id,
                        job_type=db_job.job_type,
                        reference_id=db_job.reference_id,
                        cron_expression=db_job.cron_expression,
                        scheduled_at=db_job.scheduled_at,
                        is_active=db_job.is_active,
                        run_count=db_job.run_count,
                        last_run_at=db_job.last_run_at,
                        config=db_job.config,
                        created_at=db_job.created_at,
                    )

                    # Calculate next run
                    job.next_run_at = self._calculate_next_run(job)

                    if job.next_run_at:
                        self._jobs[job.id] = job

                logger.info(f"Loaded {len(self._jobs)} scheduled jobs from database")
                return len(self._jobs)

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Error loading jobs from database: {e}")
            return 0

    async def save_to_database(self, job: ScheduledJob) -> bool:
        """
        Save a scheduled job to database.

        Args:
            job: Job to save

        Returns:
            bool: True if saved successfully
        """
        if not self._get_db:
            return False

        try:
            from ..database.db import SessionLocal
            from ..database import models

            db = SessionLocal()
            try:
                # Check if job exists
                db_job = db.query(models.ScheduledJob).filter(
                    models.ScheduledJob.id == job.id
                ).first()

                if db_job:
                    # Update existing
                    db_job.job_type = job.job_type
                    db_job.reference_id = job.reference_id
                    db_job.cron_expression = job.cron_expression
                    db_job.scheduled_at = job.scheduled_at
                    db_job.is_active = job.is_active
                    db_job.last_run_at = job.last_run_at
                    db_job.next_run_at = job.next_run_at
                    db_job.run_count = job.run_count
                    db_job.config = job.config
                    db_job.updated_at = datetime.utcnow()
                else:
                    # Create new
                    db_job = models.ScheduledJob(
                        id=job.id,
                        job_type=job.job_type,
                        reference_id=job.reference_id,
                        cron_expression=job.cron_expression,
                        scheduled_at=job.scheduled_at,
                        is_active=job.is_active,
                        last_run_at=job.last_run_at,
                        next_run_at=job.next_run_at,
                        run_count=job.run_count,
                        config=job.config,
                    )
                    db.add(db_job)

                db.commit()
                return True

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Error saving job to database: {e}")
            return False


# Global instance
task_scheduler = TaskScheduler()
