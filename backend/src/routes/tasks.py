"""Tasks API Routes"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from loguru import logger

from ..database.db import get_db
from ..database import models, schemas
from ..integrations.notion_client import notion_client
from ..device_manager.manager import device_manager
from ..agents.whatsapp_agent import whatsapp_agent

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post(
    "/sync-notion",
    summary="Sync tasks from Notion",
    description="Fetch pending tasks from Notion database and sync them to local database",
    response_description="Sync result with count of tasks synced"
)
async def sync_notion_tasks(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Sync pending WhatsApp tasks from Notion database

    This endpoint fetches pending tasks from the configured Notion database
    and creates or updates them in the local SQLite database.

    **Process:**
    1. Queries Notion for tasks with status "Pending"
    2. For each task:
       - If task exists (by notion_id): updates status and priority
       - If new: creates new task record
    3. Returns count of synced tasks

    **Args:**
    - **limit** (int, optional): Maximum number of tasks to fetch (default: 10, max: 100)

    **Returns:**
    - **success** (bool): Whether sync completed successfully
    - **tasks_synced** (int): Number of tasks synchronized
    - **tasks** (list): Array of synced task objects

    **Example Request:**
    ```
    POST /api/tasks/sync-notion?limit=20
    ```

    **Example Response:**
    ```json
    {
        "success": true,
        "tasks_synced": 5,
        "tasks": [...]
    }
    ```

    **Errors:**
    - **500**: Notion API error or database error
    - **401**: Invalid Notion API key (check .env)

    **Note:** Requires NOTION_API_KEY and NOTION_DATABASE_ID in .env
    """
    try:
        logger.info(f"🔄 API: Syncing tasks from Notion (limit: {limit})...")

        # Get pending tasks from Notion
        notion_tasks = await notion_client.get_pending_tasks(limit=limit)

        if not notion_tasks:
            logger.warning("⚠️ No pending tasks found in Notion")
            return {
                "success": True,
                "tasks_synced": 0,
                "message": "No pending tasks found"
            }

        # Save tasks to database
        synced_count = 0

        for notion_task in notion_tasks:
            # Check if task already exists
            existing_task = db.query(models.Task).filter(
                models.Task.notion_id == notion_task['notion_id']
            ).first()

            if existing_task:
                # Update existing task
                existing_task.status = notion_task['status']
                existing_task.priority = notion_task['priority']
                existing_task.scheduled_send_time = notion_task.get('scheduled_send_time')
            else:
                # Create new task
                new_task = models.Task(
                    notion_id=notion_task['notion_id'],
                    recipient_name=notion_task['recipient_name'],
                    phone_number=notion_task['phone_number'],
                    message_content=notion_task['message_content'],
                    status=notion_task['status'],
                    device_assignment=notion_task.get('device_assignment', 'Auto'),
                    priority=notion_task.get('priority', 5),
                    created_date=notion_task.get('created_date'),
                    scheduled_send_time=notion_task.get('scheduled_send_time'),
                    attempt_count=notion_task.get('attempt_count', 0),
                    notes=notion_task.get('notes', '')
                )
                db.add(new_task)

            synced_count += 1

        db.commit()

        logger.success(f"✅ API: Synced {synced_count} tasks from Notion")
        return {
            "success": True,
            "tasks_synced": synced_count,
            "tasks": notion_tasks
        }

    except Exception as e:
        logger.error(f"❌ API error syncing Notion tasks: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/run",
    summary="Execute a WhatsApp task",
    description="Run a single WhatsApp message sending task",
    response_description="Task execution result with success/failure status"
)
async def run_task(
    task_id: Optional[str] = None,
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Execute a WhatsApp message sending task

    This endpoint triggers execution of a WhatsApp message sending task.
    The task is executed using the WhatsApp Agent with DroidRun AI automation.

    **Process:**
    1. Fetches task from database (by ID or next pending with highest priority)
    2. Assigns task to available device (Auto or specific device)
    3. Updates task status to "Running"
    4. Executes WhatsApp message send:
       - Opens WhatsApp on device
       - Finds contact by phone number
       - Types message with human-like behavior
       - Sends message
       - Verifies delivery
    5. Updates Notion with result
    6. Sends Telegram notification
    7. Returns execution result

    **Args:**
    - **task_id** (int, optional): Specific task ID to run. If not provided, runs next pending task (highest priority)

    **Returns:**
    - **success** (bool): Whether task executed successfully
    - **task_id** (int): ID of executed task
    - **status** (str): Final task status ("Sent" or "Failed")
    - **device_id** (str): Device that executed the task
    - **duration_seconds** (float): Execution duration
    - **error** (str, optional): Error message if failed

    **Example Request (Auto-select next task):**
    ```
    POST /api/tasks/run
    ```

    **Example Request (Specific task):**
    ```
    POST /api/tasks/run?task_id=123
    ```

    **Example Success Response:**
    ```json
    {
        "success": true,
        "task_id": 123,
        "status": "Sent",
        "device_id": "pixel-th-1",
        "duration_seconds": 45.2
    }
    ```

    **Example Error Response:**
    ```json
    {
        "success": false,
        "task_id": 123,
        "status": "Failed",
        "error": "Invalid phone number format: abc",
        "duration_seconds": 2.1
    }
    ```

    **Errors:**
    - **404**: No pending tasks found OR task not found
    - **400**: Task is already running
    - **503**: No available devices
    - **500**: Internal error during execution

    **Real-time Updates:**
    - WebSocket broadcasts task progress to connected clients
    - Events: `task_started`, `task_progress`, `task_completed`, `task_failed`

    **Note:**
    - Execution is synchronous in MVP (Slice 1)
    - Background execution will be added in Slice 2 with queue manager
    """
    try:
        logger.info(f"▶️ API: Running task (task_id: {task_id})...")

        # Get task
        if task_id:
            task = db.query(models.Task).filter(models.Task.id == task_id).first()
            if not task:
                raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")
        else:
            # Get next pending task (highest priority)
            task = db.query(models.Task).filter(
                models.Task.status == "Pending"
            ).order_by(models.Task.priority.desc()).first()

            if not task:
                raise HTTPException(status_code=404, detail="No pending tasks found")

        # Check if task is already running
        if task.status == "Running":
            raise HTTPException(status_code=400, detail="Task is already running")

        # Select device
        device = None
        if task.device_assignment and task.device_assignment != "Auto":
            device = device_manager.devices.get(task.device_assignment)
        else:
            # Auto-assign to available device
            device = device_manager.get_available_device()  # Not async - removed await

        if not device:
            raise HTTPException(status_code=503, detail="No available devices")

        # Update task status
        task.status = "Running"
        task.device_id = device.id
        task.started_at = datetime.utcnow()
        db.commit()

        # Execute task in background
        logger.info(f"🚀 Starting task execution: {task.id}")

        # For MVP, we'll execute synchronously
        # In Slice 2, we'll use background tasks and queue
        result = await _execute_task(task, device, db)

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ API error running task: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/",
    response_model=List[schemas.TaskResponse],
    summary="List all tasks",
    description="Retrieve tasks with optional filtering by status and device"
)
async def get_tasks(
    status: Optional[str] = None,
    device_id: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    List all WhatsApp tasks with optional filtering

    Returns a list of tasks, ordered by creation date (newest first).
    Supports filtering by status and device assignment.

    **Args:**
    - **status** (str, optional): Filter by task status
      - Valid values: "Pending", "Running", "Sent", "Failed"
    - **device_id** (str, optional): Filter by assigned device ID
      - Example: "pixel-th-1"
    - **limit** (int, optional): Maximum tasks to return (default: 50, max: 1000)

    **Returns:**
    Array of task objects with full details

    **Example Request (All tasks):**
    ```
    GET /api/tasks
    ```

    **Example Request (Only pending):**
    ```
    GET /api/tasks?status=Pending&limit=20
    ```

    **Example Request (By device):**
    ```
    GET /api/tasks?device_id=pixel-th-1
    ```

    **Example Response:**
    ```json
    [
        {
            "id": "123",
            "task_type": "whatsapp",
            "status": "Sent",
            "device_id": "pixel-th-1",
            "content": {...},
            "created_at": "2025-12-04T10:00:00",
            "attempt_count": 1
        }
    ]
    ```

    **Errors:**
    - **500**: Database error

    **Note:** Results are paginated with limit parameter
    """
    try:
        logger.info(f"📋 API: Getting tasks (status: {status}, device: {device_id})...")

        query = db.query(models.Task)

        if status:
            query = query.filter(models.Task.status == status)

        if device_id:
            query = query.filter(models.Task.device_id == device_id)

        tasks = query.order_by(models.Task.created_at.desc()).limit(limit).all()

        logger.success(f"✅ API: Returned {len(tasks)} tasks")
        return tasks

    except Exception as e:
        logger.error(f"❌ API error getting tasks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{task_id}",
    response_model=schemas.TaskResponse,
    summary="Get task by ID",
    description="Retrieve detailed information about a specific task"
)
async def get_task(task_id: str, db: Session = Depends(get_db)):
    """
    Get task details by ID

    **Args:**
    - **task_id** (int): Unique task identifier

    **Returns:**
    Task object with full details

    **Example:**
    ```
    GET /api/tasks/123
    ```

    **Errors:**
    - **404**: Task not found
    - **500**: Database error
    """
    try:
        task = db.query(models.Task).filter(models.Task.id == task_id).first()

        if not task:
            raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")

        return task

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ API error getting task: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/{task_id}",
    summary="Delete task",
    description="Remove a task from the database"
)
async def delete_task(task_id: str, db: Session = Depends(get_db)):
    """
    Delete a task permanently

    **Args:**
    - **task_id** (int): Task ID to delete

    **Returns:**
    Success confirmation

    **Example:**
    ```
    DELETE /api/tasks/123
    ```

    **Example Response:**
    ```json
    {
        "success": true,
        "message": "Task deleted successfully",
        "task_id": 123
    }
    ```

    **Errors:**
    - **404**: Task not found
    - **500**: Database error

    **Warning:** This action is permanent and cannot be undone
    """
    try:
        task = db.query(models.Task).filter(models.Task.id == task_id).first()

        if not task:
            raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")

        db.delete(task)
        db.commit()

        logger.success(f"✅ API: Deleted task {task_id}")
        return {"success": True, "message": f"Task {task_id} deleted"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ API error deleting task: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def _execute_task(task: models.Task, device, db: Session) -> dict:
    """
    Execute a WhatsApp task

    Args:
        task: Task model instance
        device: Device instance
        db: Database session

    Returns:
        dict: Execution result
    """
    try:
        logger.info(f"⚡ Executing task {task.id}: {task.recipient_name}")

        # Send WhatsApp message
        result = await whatsapp_agent.send_message(
            device=device,
            recipient=task.phone_number,
            message=task.message_content,
            task_id=str(task.id),
            recipient_name=task.recipient_name,
            personalize=False,  # MVP: no personalization
            use_typos=False,  # MVP: no typos
            attempt_count=task.attempt_count + 1
        )

        # Update task based on result
        if result.get("success"):
            task.status = "Sent"
            task.sent_date = datetime.utcnow()
            task.completed_at = datetime.utcnow()
            task.notes = result.get("timestamp", "")

            # Update Notion
            if task.notion_id:
                await notion_client.update_task_status(
                    notion_id=task.notion_id,
                    status="Sent",
                    sent_date=task.sent_date.isoformat(),
                    notes=f"Sent successfully via {device.name}"
                )

            # Create success log
            log = models.Log(
                device_id=device.id,
                task_id=task.id,
                action="whatsapp_send",
                status="success"
            )
            db.add(log)

        else:
            task.status = "Failed"
            task.attempt_count += 1
            task.completed_at = datetime.utcnow()
            task.notes = result.get("error", "Unknown error")

            # Update Notion
            if task.notion_id:
                await notion_client.update_task_status(
                    notion_id=task.notion_id,
                    status="Failed",
                    notes=f"Failed: {result.get('error')}"
                )

            # Create error log
            log = models.Log(
                device_id=device.id,
                task_id=task.id,
                action="whatsapp_send",
                status="failed",
                error_message=result.get("error", "Unknown error")
            )
            db.add(log)

        db.commit()

        return {
            "success": result.get("success", False),
            "task_id": task.id,
            "status": task.status,
            "result": result
        }

    except Exception as e:
        logger.error(f"❌ Error executing task {task.id}: {e}")
        task.status = "Failed"
        task.attempt_count += 1
        task.notes = str(e)
        db.commit()

        return {
            "success": False,
            "task_id": task.id,
            "error": str(e)
        }
