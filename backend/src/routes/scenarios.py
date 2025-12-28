"""Scenarios API Routes - CRUD and execution endpoints for automation scenarios"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from loguru import logger

from ..database.db import get_db
from ..database import models, schemas
from ..orchestration.scenario_runner import scenario_runner
from ..orchestration.queue_manager import queue_manager
from ..orchestration.task_scheduler import task_scheduler


router = APIRouter(prefix="/api/scenarios", tags=["scenarios"])


# ============================================
# SCENARIO CRUD ENDPOINTS
# ============================================

@router.get(
    "/",
    response_model=List[schemas.ScenarioListResponse],
    summary="List all scenarios",
    description="Get a list of all scenarios with optional filtering"
)
async def list_scenarios(
    status: Optional[str] = None,
    device_id: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    List all scenarios with optional filtering.

    **Args:**
    - **status**: Filter by scenario status (draft, pending, running, etc.)
    - **device_id**: Filter by assigned device
    - **limit**: Maximum results (default: 50, max: 200)
    - **offset**: Pagination offset

    **Returns:**
    List of scenarios (without step details for performance)
    """
    try:
        query = db.query(models.Scenario)

        if status:
            query = query.filter(models.Scenario.status == status)
        if device_id:
            query = query.filter(models.Scenario.device_id == device_id)

        scenarios = query.order_by(
            models.Scenario.updated_at.desc()
        ).offset(offset).limit(min(limit, 200)).all()

        logger.info(f"📋 Listed {len(scenarios)} scenarios")
        return scenarios

    except Exception as e:
        logger.error(f"Error listing scenarios: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/",
    response_model=schemas.ScenarioResponse,
    status_code=201,
    summary="Create a new scenario",
    description="Create a new automation scenario with optional steps"
)
async def create_scenario(
    scenario_data: schemas.ScenarioCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new scenario.

    **Args:**
    - **scenario_data**: Scenario configuration including name, description, scheduling, and optional steps

    **Returns:**
    Created scenario with generated ID
    """
    try:
        # Create scenario
        scenario = models.Scenario(
            id=str(uuid.uuid4()),
            name=scenario_data.name,
            description=scenario_data.description,
            device_id=scenario_data.device_id,
            priority=scenario_data.priority,
            cron_expression=scenario_data.cron_expression,
            scheduled_at=scenario_data.scheduled_at,
            repeat_count=scenario_data.repeat_count,
            min_interval_seconds=scenario_data.min_interval_seconds,
            max_interval_seconds=scenario_data.max_interval_seconds,
            notion_campaign_id=scenario_data.notion_campaign_id,
            config=scenario_data.config,
            status=models.ScenarioStatus.DRAFT.value,
        )

        db.add(scenario)

        # Create steps if provided
        if scenario_data.steps:
            for step_data in scenario_data.steps:
                step = models.ScenarioStep(
                    id=str(uuid.uuid4()),
                    scenario_id=scenario.id,
                    name=step_data.name,
                    agent_type=step_data.agent_type.value,
                    action=step_data.action,
                    order=step_data.order,
                    config=step_data.config,
                    prompt_template_id=step_data.prompt_template_id,
                    delay_before_seconds=step_data.delay_before_seconds,
                    timeout_seconds=step_data.timeout_seconds,
                    max_attempts=step_data.max_attempts,
                    condition=step_data.condition,
                    skip_on_failure=step_data.skip_on_failure,
                )
                db.add(step)

            scenario.total_steps = len(scenario_data.steps)

        db.commit()
        db.refresh(scenario)

        logger.success(f"✅ Created scenario: {scenario.name} (id: {scenario.id})")
        return scenario

    except Exception as e:
        db.rollback()
        logger.error(f"Error creating scenario: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{scenario_id}",
    response_model=schemas.ScenarioResponse,
    summary="Get scenario details",
    description="Get detailed information about a specific scenario including all steps"
)
async def get_scenario(
    scenario_id: str,
    db: Session = Depends(get_db)
):
    """
    Get scenario details by ID.

    **Args:**
    - **scenario_id**: Unique scenario identifier

    **Returns:**
    Scenario with all step details
    """
    scenario = db.query(models.Scenario).filter(
        models.Scenario.id == scenario_id
    ).first()

    if not scenario:
        raise HTTPException(status_code=404, detail=f"Scenario not found: {scenario_id}")

    return scenario


@router.put(
    "/{scenario_id}",
    response_model=schemas.ScenarioResponse,
    summary="Update scenario",
    description="Update scenario configuration (cannot update while running)"
)
async def update_scenario(
    scenario_id: str,
    update_data: schemas.ScenarioUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a scenario.

    **Args:**
    - **scenario_id**: Scenario ID to update
    - **update_data**: Fields to update (partial update supported)

    **Returns:**
    Updated scenario

    **Note:** Cannot update a running scenario
    """
    scenario = db.query(models.Scenario).filter(
        models.Scenario.id == scenario_id
    ).first()

    if not scenario:
        raise HTTPException(status_code=404, detail=f"Scenario not found: {scenario_id}")

    if scenario.status == models.ScenarioStatus.RUNNING.value:
        raise HTTPException(status_code=400, detail="Cannot update a running scenario")

    try:
        # Update only provided fields
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(scenario, field, value)

        scenario.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(scenario)

        logger.success(f"✅ Updated scenario: {scenario.id}")
        return scenario

    except Exception as e:
        db.rollback()
        logger.error(f"Error updating scenario: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/{scenario_id}",
    summary="Delete scenario",
    description="Delete a scenario and all its steps"
)
async def delete_scenario(
    scenario_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a scenario.

    **Args:**
    - **scenario_id**: Scenario ID to delete

    **Returns:**
    Success confirmation

    **Warning:** This action is permanent. Cannot delete a running scenario.
    """
    scenario = db.query(models.Scenario).filter(
        models.Scenario.id == scenario_id
    ).first()

    if not scenario:
        raise HTTPException(status_code=404, detail=f"Scenario not found: {scenario_id}")

    if scenario.status == models.ScenarioStatus.RUNNING.value:
        raise HTTPException(status_code=400, detail="Cannot delete a running scenario")

    try:
        db.delete(scenario)  # Cascades to steps
        db.commit()

        logger.success(f"✅ Deleted scenario: {scenario_id}")
        return {"success": True, "message": f"Scenario {scenario_id} deleted"}

    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting scenario: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# SCENARIO EXECUTION ENDPOINTS
# ============================================

@router.post(
    "/{scenario_id}/run",
    summary="Run scenario",
    description="Start executing a scenario"
)
async def run_scenario(
    scenario_id: str,
    run_request: schemas.ScenarioRunRequest = None,
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Start executing a scenario.

    **Args:**
    - **scenario_id**: Scenario to run
    - **device_id** (optional): Override default device
    - **skip_to_step** (optional): Skip to specific step number
    - **dry_run** (optional): Test mode without actual execution

    **Returns:**
    Execution status

    **Real-time Updates:**
    Progress is broadcasted via WebSocket events:
    - scenario_started
    - step_started
    - step_completed
    - step_failed
    - scenario_completed
    """
    scenario = db.query(models.Scenario).filter(
        models.Scenario.id == scenario_id
    ).first()

    if not scenario:
        raise HTTPException(status_code=404, detail=f"Scenario not found: {scenario_id}")

    if scenario.status == models.ScenarioStatus.RUNNING.value:
        raise HTTPException(status_code=400, detail="Scenario is already running")

    if not scenario.steps:
        raise HTTPException(status_code=400, detail="Scenario has no steps")

    request = run_request or schemas.ScenarioRunRequest()

    try:
        # Run in background
        if background_tasks:
            background_tasks.add_task(
                scenario_runner.run_scenario,
                scenario_id=scenario_id,
                device_id=request.device_id,
                skip_to_step=request.skip_to_step,
                dry_run=request.dry_run
            )

            logger.info(f"▶️ Started scenario (background): {scenario_id}")
            return {
                "success": True,
                "message": "Scenario started",
                "scenario_id": scenario_id,
                "dry_run": request.dry_run,
            }

        # Run synchronously (for testing)
        result = await scenario_runner.run_scenario(
            scenario_id=scenario_id,
            device_id=request.device_id,
            skip_to_step=request.skip_to_step,
            dry_run=request.dry_run
        )

        return result

    except Exception as e:
        logger.error(f"Error starting scenario: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/{scenario_id}/pause",
    summary="Pause scenario",
    description="Pause a running scenario"
)
async def pause_scenario(scenario_id: str):
    """
    Pause a running scenario.

    **Args:**
    - **scenario_id**: Scenario to pause

    **Returns:**
    Success status
    """
    success = await scenario_runner.pause_scenario(scenario_id)

    if not success:
        raise HTTPException(status_code=400, detail="Cannot pause scenario (not running)")

    return {"success": True, "message": "Scenario paused"}


@router.post(
    "/{scenario_id}/resume",
    summary="Resume scenario",
    description="Resume a paused scenario"
)
async def resume_scenario(scenario_id: str):
    """
    Resume a paused scenario.

    **Args:**
    - **scenario_id**: Scenario to resume

    **Returns:**
    Success status
    """
    success = await scenario_runner.resume_scenario(scenario_id)

    if not success:
        raise HTTPException(status_code=400, detail="Cannot resume scenario (not paused)")

    return {"success": True, "message": "Scenario resumed"}


@router.post(
    "/{scenario_id}/cancel",
    summary="Cancel scenario",
    description="Cancel a running or paused scenario"
)
async def cancel_scenario(scenario_id: str):
    """
    Cancel a running or paused scenario.

    **Args:**
    - **scenario_id**: Scenario to cancel

    **Returns:**
    Success status
    """
    success = await scenario_runner.cancel_scenario(scenario_id)

    if not success:
        raise HTTPException(status_code=400, detail="Cannot cancel scenario (not running or paused)")

    return {"success": True, "message": "Scenario cancellation requested"}


# ============================================
# STEP MANAGEMENT ENDPOINTS
# ============================================

@router.get(
    "/{scenario_id}/steps",
    response_model=List[schemas.ScenarioStepResponse],
    summary="Get scenario steps",
    description="Get all steps for a scenario"
)
async def get_steps(
    scenario_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all steps for a scenario, ordered by execution order.

    **Args:**
    - **scenario_id**: Scenario ID

    **Returns:**
    List of steps
    """
    scenario = db.query(models.Scenario).filter(
        models.Scenario.id == scenario_id
    ).first()

    if not scenario:
        raise HTTPException(status_code=404, detail=f"Scenario not found: {scenario_id}")

    return sorted(scenario.steps, key=lambda s: s.order)


@router.post(
    "/{scenario_id}/steps",
    response_model=schemas.ScenarioStepResponse,
    status_code=201,
    summary="Add step to scenario",
    description="Add a new step to a scenario"
)
async def add_step(
    scenario_id: str,
    step_data: schemas.ScenarioStepCreate,
    db: Session = Depends(get_db)
):
    """
    Add a new step to a scenario.

    **Args:**
    - **scenario_id**: Scenario to add step to
    - **step_data**: Step configuration

    **Returns:**
    Created step
    """
    scenario = db.query(models.Scenario).filter(
        models.Scenario.id == scenario_id
    ).first()

    if not scenario:
        raise HTTPException(status_code=404, detail=f"Scenario not found: {scenario_id}")

    if scenario.status == models.ScenarioStatus.RUNNING.value:
        raise HTTPException(status_code=400, detail="Cannot modify a running scenario")

    try:
        step = models.ScenarioStep(
            id=str(uuid.uuid4()),
            scenario_id=scenario_id,
            name=step_data.name,
            agent_type=step_data.agent_type.value,
            action=step_data.action,
            order=step_data.order,
            config=step_data.config,
            prompt_template_id=step_data.prompt_template_id,
            delay_before_seconds=step_data.delay_before_seconds,
            timeout_seconds=step_data.timeout_seconds,
            max_attempts=step_data.max_attempts,
            condition=step_data.condition,
            skip_on_failure=step_data.skip_on_failure,
        )

        db.add(step)
        scenario.total_steps = len(scenario.steps) + 1
        scenario.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(step)

        logger.success(f"✅ Added step to scenario {scenario_id}: {step.name}")
        return step

    except Exception as e:
        db.rollback()
        logger.error(f"Error adding step: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/{scenario_id}/steps/{step_id}",
    response_model=schemas.ScenarioStepResponse,
    summary="Update step",
    description="Update a step in a scenario"
)
async def update_step(
    scenario_id: str,
    step_id: str,
    update_data: schemas.ScenarioStepUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a step.

    **Args:**
    - **scenario_id**: Scenario ID
    - **step_id**: Step ID to update
    - **update_data**: Fields to update

    **Returns:**
    Updated step
    """
    step = db.query(models.ScenarioStep).filter(
        models.ScenarioStep.id == step_id,
        models.ScenarioStep.scenario_id == scenario_id
    ).first()

    if not step:
        raise HTTPException(status_code=404, detail=f"Step not found: {step_id}")

    scenario = step.scenario
    if scenario.status == models.ScenarioStatus.RUNNING.value:
        raise HTTPException(status_code=400, detail="Cannot modify a running scenario")

    try:
        update_dict = update_data.model_dump(exclude_unset=True)

        # Handle enum conversion
        if "agent_type" in update_dict and update_dict["agent_type"]:
            update_dict["agent_type"] = update_dict["agent_type"].value

        for field, value in update_dict.items():
            setattr(step, field, value)

        scenario.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(step)

        logger.success(f"✅ Updated step: {step_id}")
        return step

    except Exception as e:
        db.rollback()
        logger.error(f"Error updating step: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/{scenario_id}/steps/{step_id}",
    summary="Delete step",
    description="Remove a step from a scenario"
)
async def delete_step(
    scenario_id: str,
    step_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a step from a scenario.

    **Args:**
    - **scenario_id**: Scenario ID
    - **step_id**: Step ID to delete

    **Returns:**
    Success confirmation
    """
    step = db.query(models.ScenarioStep).filter(
        models.ScenarioStep.id == step_id,
        models.ScenarioStep.scenario_id == scenario_id
    ).first()

    if not step:
        raise HTTPException(status_code=404, detail=f"Step not found: {step_id}")

    scenario = step.scenario
    if scenario.status == models.ScenarioStatus.RUNNING.value:
        raise HTTPException(status_code=400, detail="Cannot modify a running scenario")

    try:
        db.delete(step)
        scenario.total_steps = max(0, scenario.total_steps - 1)
        scenario.updated_at = datetime.utcnow()
        db.commit()

        logger.success(f"✅ Deleted step: {step_id}")
        return {"success": True, "message": f"Step {step_id} deleted"}

    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting step: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# SCHEDULER ENDPOINTS
# ============================================

@router.post(
    "/{scenario_id}/schedule",
    summary="Schedule scenario",
    description="Schedule a scenario for automatic execution"
)
async def schedule_scenario(
    scenario_id: str,
    db: Session = Depends(get_db)
):
    """
    Schedule a scenario for automatic execution based on its cron_expression or scheduled_at.

    **Args:**
    - **scenario_id**: Scenario to schedule

    **Returns:**
    Scheduling status
    """
    scenario = db.query(models.Scenario).filter(
        models.Scenario.id == scenario_id
    ).first()

    if not scenario:
        raise HTTPException(status_code=404, detail=f"Scenario not found: {scenario_id}")

    if not scenario.cron_expression and not scenario.scheduled_at:
        raise HTTPException(
            status_code=400,
            detail="Scenario has no schedule configured (set cron_expression or scheduled_at)"
        )

    try:
        job = await task_scheduler.add_job(
            job_id=f"scenario_{scenario_id}",
            job_type="scenario",
            reference_id=scenario_id,
            cron_expression=scenario.cron_expression,
            scheduled_at=scenario.scheduled_at,
            repeat_count=scenario.repeat_count,
            callback=scenario_runner.run_scenario,
            callback_kwargs={"scenario_id": scenario_id},
            config={"priority": scenario.priority}
        )

        # Update scenario status
        scenario.status = models.ScenarioStatus.PENDING.value
        scenario.next_run_at = job.next_run_at
        db.commit()

        logger.success(f"✅ Scheduled scenario: {scenario_id}")
        return {
            "success": True,
            "message": "Scenario scheduled",
            "next_run_at": job.next_run_at.isoformat() if job.next_run_at else None
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error scheduling scenario: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/{scenario_id}/schedule",
    summary="Unschedule scenario",
    description="Remove scenario from automatic scheduling"
)
async def unschedule_scenario(
    scenario_id: str,
    db: Session = Depends(get_db)
):
    """
    Remove a scenario from automatic scheduling.

    **Args:**
    - **scenario_id**: Scenario to unschedule

    **Returns:**
    Success status
    """
    success = await task_scheduler.remove_job(f"scenario_{scenario_id}")

    if success:
        scenario = db.query(models.Scenario).filter(
            models.Scenario.id == scenario_id
        ).first()

        if scenario:
            scenario.status = models.ScenarioStatus.DRAFT.value
            scenario.next_run_at = None
            db.commit()

    return {"success": success, "message": "Scenario unscheduled" if success else "Scenario was not scheduled"}


# ============================================
# QUEUE STATUS ENDPOINTS
# ============================================

@router.get(
    "/queue/status",
    response_model=schemas.SchedulerStatusResponse,
    summary="Get queue status",
    description="Get current queue and scheduler status"
)
async def get_queue_status():
    """
    Get current status of the queue and scheduler.

    **Returns:**
    - Queue statistics (queued, processing, completed, failed)
    - Scheduler status
    - Next scheduled job
    """
    queue_status = queue_manager.get_queue_status()
    scheduler_status = task_scheduler.get_status()

    return schemas.SchedulerStatusResponse(
        is_running=scheduler_status["is_running"],
        active_jobs=scheduler_status["active_jobs"],
        queued_jobs=queue_status["queued_count"],
        completed_today=queue_status["stats"]["total_completed"],
        failed_today=queue_status["stats"]["total_failed"],
        next_scheduled_job=scheduler_status.get("next_job")
    )


@router.get(
    "/queue/items",
    response_model=List[schemas.QueuedTaskResponse],
    summary="Get queued items",
    description="Get list of items currently in the queue"
)
async def get_queued_items(limit: int = 50):
    """
    Get items currently in the queue.

    **Args:**
    - **limit**: Maximum items to return

    **Returns:**
    List of queued items
    """
    items = queue_manager.get_queued_items(limit=limit)

    return [
        schemas.QueuedTaskResponse(
            id=item["id"],
            type=item["type"],
            reference_id=item["reference_id"],
            priority=item["priority"],
            status=item["status"],
            queued_at=datetime.fromisoformat(item["queued_at"]),
        )
        for item in items
    ]
