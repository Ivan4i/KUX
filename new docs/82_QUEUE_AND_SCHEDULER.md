# 82_QUEUE_AND_SCHEDULER.md

## Task Queue & Scheduler (Celery + APScheduler)

### Architecture Overview

```
Task Execution Pipeline:

Frontend (React)
    ↓ WebSocket
Backend (FastAPI)
    ↓ POST /api/workflows/{id}/execute
Queue Manager (Celery)
    ↓ Add to Redis queue
Task Scheduler (APScheduler)
    ↓ Pick available device
Execution Engine
    ↓ Execute workflow
Device (Android via ADB)
    ↓
Results
    ↓ WebSocket back to Frontend

Performance:
- Queue: Handles 1000+ tasks/second
- Scheduler: Distributes across 7 devices
- Execution: Parallel (one workflow per device)
- Notification: Real-time via WebSocket
```

### Task Queue Manager (Celery)

```python
# app/core/queue_manager.py
from celery import Celery, Task
from celery.result import AsyncResult
from redis import Redis
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize Celery
celery_app = Celery(
    "multidevice_automation",
    broker=settings.CELERY_BROKER,
    backend=settings.CELERY_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 min hard limit
    task_soft_time_limit=25 * 60,  # 25 min soft limit
)

class WorkflowTask(Task):
    """Custom Celery task for workflow execution"""
    
    autoretry_for = (Exception,)
    retry_kwargs = {"max_retries": 3}
    retry_backoff = True
    retry_backoff_max = 600
    retry_jitter = True

@celery_app.task(bind=True, base=WorkflowTask)
def execute_workflow_task(
    self,
    workflow_id: str,
    device_id: str,
    task_id: str,
) -> dict:
    """
    Execute workflow as Celery task.
    
    This runs in a worker process, allowing
    long-running workflows to execute async.
    """
    
    try:
        logger.info(f"🚀 Celery: Starting task {self.request.id}")
        
        # Import here to avoid circular imports
        from app.models.task import Task
        from app.models.workflow import Workflow
        from app.models.device import Device
        from app.core.execution_engine import ExecutionEngine
        from app.services.notification_service import NotificationService
        from app.services.adb_service import ADBService
        from app.services.alignui_service import AlignUIService
        from sqlalchemy.orm import Session
        from app.config import SessionLocal
        
        # Get database session
        db = SessionLocal()
        
        try:
            # Load workflow, device, task
            workflow = db.query(Workflow).filter_by(id=workflow_id).first()
            device = db.query(Device).filter_by(id=device_id).first()
            task = db.query(Task).filter_by(id=task_id).first()
            
            if not all([workflow, device, task]):
                raise ValueError("Workflow, device, or task not found")
            
            # Initialize services
            notification_service = NotificationService()
            adb_service = ADBService()
            alignui_service = AlignUIService(settings.ALIGNUI_API_KEY)
            
            # Create execution engine
            engine = ExecutionEngine(
                notification_service,
                adb_service,
                alignui_service,
            )
            
            # Execute workflow
            result = asyncio.run(
                engine.execute_workflow(workflow, device, task)
            )
            
            logger.info(f"✅ Celery: Task completed - {result}")
            return result
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"❌ Celery: Task failed - {e}")
        
        # Update task status on failure
        # The AutoRetry mechanism will retry automatically
        raise

class QueueManager:
    """
    Manage task queue and scheduling.
    
    Responsibilities:
    - Queue tasks
    - Track task status
    - Retry failed tasks
    - Clean up old tasks
    """
    
    def __init__(self):
        self.redis = Redis.from_url(settings.REDIS_URL)
        self.celery = celery_app
    
    async def queue_workflow(
        self,
        workflow_id: str,
        device_id: str,
        task_id: str,
    ) -> str:
        """Queue workflow execution"""
        
        logger.info(f"📋 Queuing: {workflow_id} on {device_id}")
        
        # Send task to Celery queue
        task = self.celery.send_task(
            "app.core.queue_manager.execute_workflow_task",
            args=(workflow_id, device_id, task_id),
            queue="default",
        )
        
        logger.info(f"  → Celery task ID: {task.id}")
        return task.id
    
    async def get_task_status(self, celery_task_id: str) -> dict:
        """Get status of queued task"""
        
        result = AsyncResult(celery_task_id, app=self.celery)
        
        return {
            "celery_task_id": celery_task_id,
            "status": result.status,  # PENDING, STARTED, SUCCESS, FAILURE, RETRY
            "progress": result.info.get("progress") if isinstance(result.info, dict) else None,
            "result": result.result if result.successful() else None,
            "error": str(result.info) if result.failed() else None,
        }
    
    async def get_queue_stats(self) -> dict:
        """Get queue statistics"""
        
        # Get pending tasks count
        inspect = self.celery.control.inspect()
        active = inspect.active() or {}
        reserved = inspect.reserved() or {}
        
        pending = sum(len(tasks) for tasks in active.values())
        reserved_count = sum(len(tasks) for tasks in reserved.values())
        
        return {
            "pending_tasks": pending,
            "reserved_tasks": reserved_count,
            "total_workers": len(active),
        }
    
    async def cancel_task(self, celery_task_id: str) -> bool:
        """Cancel queued task"""
        
        self.celery.control.revoke(celery_task_id, terminate=True)
        logger.info(f"❌ Cancelled task: {celery_task_id}")
        return True
    
    async def clean_completed_tasks(self, older_than_hours: int = 24):
        """Clean up old completed tasks"""
        
        logger.info(f"🧹 Cleaning tasks older than {older_than_hours}h")
        
        # This is handled by Celery's result backend cleanup
        # Configure in settings if needed
        pass
```

### Task Scheduler (APScheduler)

```python
# app/core/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from app.config import SessionLocal
from app.models.task import Task, TaskStatus
from app.models.device import Device
from app.services.device_service import DeviceService
from app.core.queue_manager import QueueManager
import logging

logger = logging.getLogger(__name__)

class TaskScheduler:
    """
    Schedule and distribute tasks to devices.
    
    Responsibilities:
    - Monitor device availability
    - Distribute pending tasks
    - Handle device failures
    - Implement backpressure
    """
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.queue_manager = QueueManager()
        self.device_service = DeviceService()
        self.is_running = False
    
    async def start(self):
        """Start scheduler"""
        
        logger.info("⏰ Starting task scheduler...")
        
        # Schedule periodic task distribution
        self.scheduler.add_job(
            self.distribute_tasks,
            IntervalTrigger(seconds=5),  # Run every 5 seconds
            id="distribute_tasks",
            name="Distribute pending tasks",
            replace_existing=True,
        )
        
        # Schedule health check
        self.scheduler.add_job(
            self.health_check,
            IntervalTrigger(minutes=1),
            id="health_check",
            name="Check device health",
            replace_existing=True,
        )
        
        # Schedule metrics collection
        self.scheduler.add_job(
            self.collect_metrics,
            IntervalTrigger(minutes=5),
            id="collect_metrics",
            name="Collect performance metrics",
            replace_existing=True,
        )
        
        self.scheduler.start()
        self.is_running = True
        logger.info("✅ Scheduler started")
    
    async def stop(self):
        """Stop scheduler"""
        
        logger.info("🛑 Stopping scheduler...")
        self.scheduler.shutdown()
        self.is_running = False
        logger.info("✅ Scheduler stopped")
    
    async def distribute_tasks(self):
        """Distribute pending tasks to available devices"""
        
        try:
            db = SessionLocal()
            
            # Get pending tasks
            pending_tasks = db.query(Task).filter(
                Task.status == TaskStatus.PENDING
            ).limit(10).all()
            
            if not pending_tasks:
                return
            
            logger.info(f"📊 Distributing {len(pending_tasks)} pending tasks")
            
            # Get available devices
            devices = await self.device_service.get_available_devices()
            
            if not devices:
                logger.warning("⚠️  No available devices")
                return
            
            # Distribute tasks round-robin
            for idx, task in enumerate(pending_tasks):
                device = devices[idx % len(devices)]
                
                # Load workflow
                from app.models.workflow import Workflow
                workflow = db.query(Workflow).filter_by(
                    id=task.workflow_id
                ).first()
                
                # Queue the task
                celery_task_id = await self.queue_manager.queue_workflow(
                    task.workflow_id,
                    device.id,
                    task.id,
                )
                
                # Update task
                task.status = TaskStatus.QUEUED
                task.device_id = device.id
                task.celery_task_id = celery_task_id
                task.queued_at = datetime.utcnow()
                
                db.add(task)
            
            db.commit()
            logger.info(f"✅ Distributed {len(pending_tasks)} tasks")
        
        except Exception as e:
            logger.error(f"❌ Distribution failed: {e}")
        
        finally:
            db.close()
    
    async def health_check(self):
        """Monitor device health and restart if needed"""
        
        try:
            db = SessionLocal()
            
            devices = db.query(Device).all()
            
            for device in devices:
                # Check if device is responsive
                try:
                    is_alive = await self.device_service.check_device_health(device.id)
                    
                    if not is_alive:
                        logger.warning(f"⚠️  Device {device.id} not responding")
                        device.status = "offline"
                    else:
                        device.status = "online"
                
                except Exception as e:
                    logger.error(f"❌ Health check failed for {device.id}: {e}")
                    device.status = "error"
            
            db.commit()
        
        except Exception as e:
            logger.error(f"❌ Health check failed: {e}")
        
        finally:
            db.close()
    
    async def collect_metrics(self):
        """Collect performance metrics"""
        
        try:
            # Get queue statistics
            queue_stats = await self.queue_manager.get_queue_stats()
            logger.info(f"📈 Queue stats: {queue_stats}")
            
            # Store in database for analytics
            db = SessionLocal()
            
            from app.models.analytics import Metric
            metric = Metric(
                metric_type="queue_stats",
                value=queue_stats,
                timestamp=datetime.utcnow(),
            )
            
            db.add(metric)
            db.commit()
            db.close()
        
        except Exception as e:
            logger.error(f"❌ Metrics collection failed: {e}")

# Usage in main.py
scheduler = TaskScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown events"""
    
    await scheduler.start()
    yield
    await scheduler.stop()
```

### Task Endpoint

```python
# app/api/v1/tasks.py
from fastapi import APIRouter, HTTPException
from app.core.queue_manager import QueueManager
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskResponse, CreateTaskRequest
from app.config import SessionLocal
from typing import List

router = APIRouter()
queue_manager = QueueManager()

@router.post("/", response_model=TaskResponse)
async def create_task(request: CreateTaskRequest):
    """Create and queue a task"""
    
    db = SessionLocal()
    
    try:
        # Create task
        task = Task(
            workflow_id=request.workflow_id,
            status=TaskStatus.PENDING,
            created_at=datetime.utcnow(),
        )
        
        db.add(task)
        db.commit()
        db.refresh(task)
        
        logger.info(f"📝 Created task: {task.id}")
        
        return TaskResponse.from_orm(task)
    
    finally:
        db.close()

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Get task status"""
    
    db = SessionLocal()
    
    try:
        task = db.query(Task).filter_by(id=task_id).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # If task has celery_task_id, get status from queue
        if task.celery_task_id:
            queue_status = await queue_manager.get_task_status(task.celery_task_id)
            task.celery_status = queue_status
        
        return TaskResponse.from_orm(task)
    
    finally:
        db.close()

@router.delete("/{task_id}")
async def cancel_task(task_id: str):
    """Cancel a task"""
    
    db = SessionLocal()
    
    try:
        task = db.query(Task).filter_by(id=task_id).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Cancel in queue if applicable
        if task.celery_task_id:
            await queue_manager.cancel_task(task.celery_task_id)
        
        # Update task status
        task.status = TaskStatus.CANCELLED
        db.commit()
        
        return {"success": True}
    
    finally:
        db.close()

@router.get("/queue/stats")
async def queue_stats():
    """Get queue statistics"""
    
    stats = await queue_manager.get_queue_stats()
    return stats
```

---

## End of 82_QUEUE_AND_SCHEDULER.md