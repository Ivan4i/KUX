"""
Scenario Runner - Step-by-step scenario execution engine

Features:
- Sequential step execution with ordering
- Step-specific delays and timeouts
- Condition-based step execution
- Agent integration (WhatsApp, Instagram, etc.)
- Error handling with retries
- Real-time progress reporting via WebSocket
- Pause/Resume/Cancel support
"""

import asyncio
import random
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable, Awaitable
from enum import Enum
from loguru import logger


class ScenarioState(str, Enum):
    """Scenario execution state"""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    CANCELLING = "cancelling"


class StepResult:
    """Result of a step execution"""

    def __init__(
        self,
        success: bool,
        data: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None
    ):
        self.success = success
        self.data = data or {}
        self.error = error


class ScenarioRunner:
    """
    Executes scenarios step by step.

    Handles:
    - Sequential step execution
    - Step delays and timeouts
    - Condition checking
    - Agent dispatch
    - Error handling and retries
    - Pause/Resume/Cancel
    - Progress reporting
    """

    def __init__(self):
        """Initialize Scenario Runner"""
        # Agent registry: agent_type -> agent instance
        self._agents: Dict[str, Any] = {}

        # Active scenario states
        self._scenario_states: Dict[str, ScenarioState] = {}

        # Control events for pause/cancel
        self._pause_events: Dict[str, asyncio.Event] = {}
        self._cancel_flags: Dict[str, bool] = {}

        # WebSocket manager
        self._ws_manager = None

        # Database session factory
        self._get_db = None

        # Device manager
        self._device_manager = None

        logger.info("ScenarioRunner initialized")

    def set_websocket_manager(self, ws_manager) -> None:
        """Set WebSocket manager for real-time updates"""
        self._ws_manager = ws_manager

    def set_db_factory(self, get_db: Callable) -> None:
        """Set database session factory"""
        self._get_db = get_db

    def set_device_manager(self, device_manager) -> None:
        """Set device manager for device access"""
        self._device_manager = device_manager

    def register_agent(self, agent_type: str, agent: Any) -> None:
        """
        Register an agent for a specific type.

        Args:
            agent_type: Type identifier (e.g., 'whatsapp', 'instagram')
            agent: Agent instance
        """
        self._agents[agent_type] = agent
        logger.info(f"Registered agent: {agent_type}")

    async def run_scenario(
        self,
        scenario_id: str,
        device_id: Optional[str] = None,
        skip_to_step: Optional[int] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Run a scenario.

        Args:
            scenario_id: ID of the scenario to run
            device_id: Override device ID (optional)
            skip_to_step: Skip to specific step number (1-based)
            dry_run: Test mode - don't actually execute

        Returns:
            dict: Execution result
        """
        logger.info(f"Starting scenario: {scenario_id} (dry_run: {dry_run})")

        # Load scenario from database
        scenario = await self._load_scenario(scenario_id)
        if not scenario:
            return {"success": False, "error": f"Scenario not found: {scenario_id}"}

        # Check if already running
        if self._scenario_states.get(scenario_id) == ScenarioState.RUNNING:
            return {"success": False, "error": "Scenario is already running"}

        # Initialize state
        self._scenario_states[scenario_id] = ScenarioState.RUNNING
        self._pause_events[scenario_id] = asyncio.Event()
        self._pause_events[scenario_id].set()  # Not paused initially
        self._cancel_flags[scenario_id] = False

        # Get device
        effective_device_id = device_id or scenario.device_id
        device = await self._get_device(effective_device_id)

        if not device and not dry_run:
            return {"success": False, "error": f"Device not available: {effective_device_id}"}

        try:
            # Update scenario status
            await self._update_scenario_status(scenario_id, "running")
            await self._notify_scenario_update("scenario_started", scenario_id, {
                "device_id": effective_device_id,
                "total_steps": len(scenario.steps),
            })

            # Execute steps
            result = await self._execute_steps(
                scenario=scenario,
                device=device,
                skip_to_step=skip_to_step,
                dry_run=dry_run
            )

            # Update final status
            final_status = "completed" if result["success"] else "failed"
            await self._update_scenario_status(
                scenario_id,
                final_status,
                error_message=result.get("error")
            )

            await self._notify_scenario_update("scenario_completed", scenario_id, result)

            return result

        except asyncio.CancelledError:
            logger.info(f"Scenario {scenario_id} was cancelled")
            await self._update_scenario_status(scenario_id, "cancelled")
            return {"success": False, "error": "Scenario was cancelled"}

        except Exception as e:
            logger.error(f"Error running scenario {scenario_id}: {e}")
            await self._update_scenario_status(scenario_id, "failed", error_message=str(e))
            return {"success": False, "error": str(e)}

        finally:
            # Cleanup
            self._scenario_states[scenario_id] = ScenarioState.IDLE
            self._pause_events.pop(scenario_id, None)
            self._cancel_flags.pop(scenario_id, None)

    async def pause_scenario(self, scenario_id: str) -> bool:
        """Pause a running scenario"""
        if self._scenario_states.get(scenario_id) != ScenarioState.RUNNING:
            return False

        self._scenario_states[scenario_id] = ScenarioState.PAUSED
        self._pause_events[scenario_id].clear()  # Block execution

        await self._update_scenario_status(scenario_id, "paused")
        await self._notify_scenario_update("scenario_paused", scenario_id, {})

        logger.info(f"Paused scenario: {scenario_id}")
        return True

    async def resume_scenario(self, scenario_id: str) -> bool:
        """Resume a paused scenario"""
        if self._scenario_states.get(scenario_id) != ScenarioState.PAUSED:
            return False

        self._scenario_states[scenario_id] = ScenarioState.RUNNING
        self._pause_events[scenario_id].set()  # Unblock execution

        await self._update_scenario_status(scenario_id, "running")
        await self._notify_scenario_update("scenario_resumed", scenario_id, {})

        logger.info(f"Resumed scenario: {scenario_id}")
        return True

    async def cancel_scenario(self, scenario_id: str) -> bool:
        """Cancel a running or paused scenario"""
        state = self._scenario_states.get(scenario_id)
        if state not in (ScenarioState.RUNNING, ScenarioState.PAUSED):
            return False

        self._cancel_flags[scenario_id] = True
        self._scenario_states[scenario_id] = ScenarioState.CANCELLING

        # Unblock if paused
        if scenario_id in self._pause_events:
            self._pause_events[scenario_id].set()

        logger.info(f"Cancelling scenario: {scenario_id}")
        return True

    def get_scenario_state(self, scenario_id: str) -> Optional[ScenarioState]:
        """Get current state of a scenario"""
        return self._scenario_states.get(scenario_id)

    async def _execute_steps(
        self,
        scenario,
        device,
        skip_to_step: Optional[int] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """Execute scenario steps sequentially"""
        steps = sorted(scenario.steps, key=lambda s: s.order)
        total_steps = len(steps)
        completed_steps = 0
        failed_steps = 0
        results = []

        for step in steps:
            scenario_id = scenario.id

            # Check for cancellation
            if self._cancel_flags.get(scenario_id):
                logger.info(f"Scenario {scenario_id} cancelled at step {step.order}")
                return {
                    "success": False,
                    "error": "Cancelled by user",
                    "completed_steps": completed_steps,
                    "total_steps": total_steps,
                }

            # Wait if paused
            await self._pause_events[scenario_id].wait()

            # Skip to specific step if requested
            if skip_to_step and step.order < skip_to_step:
                logger.info(f"Skipping step {step.order} (skip_to_step: {skip_to_step})")
                await self._update_step_status(step.id, "skipped")
                continue

            # Check step condition
            if not await self._check_step_condition(step, results):
                logger.info(f"Step {step.order} condition not met, skipping")
                await self._update_step_status(step.id, "skipped")
                continue

            # Notify step start
            await self._notify_scenario_update("step_started", scenario_id, {
                "step_id": step.id,
                "step_order": step.order,
                "step_name": step.name,
                "agent_type": step.agent_type,
                "action": step.action,
            })

            # Apply delay before step
            if step.delay_before_seconds > 0 and not dry_run:
                logger.debug(f"Waiting {step.delay_before_seconds}s before step {step.order}")
                await self._interruptible_sleep(
                    scenario_id,
                    step.delay_before_seconds
                )

            # Execute step
            try:
                await self._update_step_status(step.id, "running")

                step_result = await self._execute_step(
                    step=step,
                    device=device,
                    dry_run=dry_run
                )

                results.append({
                    "step_id": step.id,
                    "order": step.order,
                    "result": step_result
                })

                if step_result.success:
                    completed_steps += 1
                    await self._update_step_status(
                        step.id, "completed",
                        result=step_result.data
                    )
                    await self._notify_scenario_update("step_completed", scenario_id, {
                        "step_id": step.id,
                        "step_order": step.order,
                        "result": step_result.data,
                    })
                else:
                    failed_steps += 1
                    await self._update_step_status(
                        step.id, "failed",
                        error_message=step_result.error
                    )
                    await self._notify_scenario_update("step_failed", scenario_id, {
                        "step_id": step.id,
                        "step_order": step.order,
                        "error": step_result.error,
                    })

                    # Check if we should continue on failure
                    if not step.skip_on_failure:
                        return {
                            "success": False,
                            "error": f"Step {step.order} failed: {step_result.error}",
                            "completed_steps": completed_steps,
                            "failed_steps": failed_steps,
                            "total_steps": total_steps,
                        }

            except asyncio.TimeoutError:
                logger.error(f"Step {step.order} timed out")
                failed_steps += 1
                await self._update_step_status(step.id, "failed", error_message="Timeout")

                if not step.skip_on_failure:
                    return {
                        "success": False,
                        "error": f"Step {step.order} timed out",
                        "completed_steps": completed_steps,
                        "failed_steps": failed_steps,
                        "total_steps": total_steps,
                    }

            # Update scenario progress
            await self._update_scenario_progress(
                scenario_id,
                current_step=step.order,
                total_steps=total_steps
            )

            # Apply random interval between steps (for campaigns)
            if step.order < total_steps:
                interval = random.randint(
                    scenario.min_interval_seconds,
                    scenario.max_interval_seconds
                )
                if interval > 0 and not dry_run:
                    logger.debug(f"Waiting {interval}s before next step")
                    await self._interruptible_sleep(scenario_id, interval)

        return {
            "success": failed_steps == 0,
            "completed_steps": completed_steps,
            "failed_steps": failed_steps,
            "total_steps": total_steps,
            "results": results,
        }

    async def _execute_step(
        self,
        step,
        device,
        dry_run: bool = False
    ) -> StepResult:
        """Execute a single step with retry logic"""
        last_error = None

        for attempt in range(step.max_attempts):
            try:
                logger.info(
                    f"Executing step: {step.name} "
                    f"(agent: {step.agent_type}, action: {step.action}, "
                    f"attempt: {attempt + 1}/{step.max_attempts})"
                )

                if dry_run:
                    # Simulate execution
                    await asyncio.sleep(0.5)
                    return StepResult(
                        success=True,
                        data={"dry_run": True, "step": step.name}
                    )

                # Get agent
                agent = self._agents.get(step.agent_type)
                if not agent:
                    return StepResult(
                        success=False,
                        error=f"Agent not registered: {step.agent_type}"
                    )

                # Execute with timeout
                result = await asyncio.wait_for(
                    self._dispatch_to_agent(agent, step, device),
                    timeout=step.timeout_seconds
                )

                return result

            except asyncio.TimeoutError:
                last_error = "Step execution timed out"
                logger.warning(f"Step {step.name} timed out (attempt {attempt + 1})")

            except Exception as e:
                last_error = str(e)
                logger.error(f"Step {step.name} failed: {e} (attempt {attempt + 1})")

            # Wait before retry
            if attempt < step.max_attempts - 1:
                await asyncio.sleep(5 * (attempt + 1))  # Increasing delay

        return StepResult(success=False, error=last_error)

    async def _dispatch_to_agent(
        self,
        agent,
        step,
        device
    ) -> StepResult:
        """Dispatch action to appropriate agent"""
        action = step.action
        config = step.config or {}

        try:
            # Common actions
            if action == "send_message":
                result = await agent.send_message(
                    device=device,
                    recipient=config.get("recipient"),
                    message=config.get("message"),
                    **config.get("options", {})
                )
                return StepResult(
                    success=result.get("success", False),
                    data=result,
                    error=result.get("error")
                )

            elif action == "open_app":
                success = await agent.open_app(device)
                return StepResult(success=success)

            elif action == "close_app":
                success = await agent.close_app(device)
                return StepResult(success=success)

            elif action == "warmup":
                # Generic warmup action
                result = await agent.warmup(
                    device=device,
                    duration_seconds=config.get("duration", 60),
                    **config.get("options", {})
                )
                return StepResult(
                    success=result.get("success", False),
                    data=result,
                    error=result.get("error")
                )

            elif action == "post_content":
                # Generic content posting (Instagram reels, etc.)
                result = await agent.post_content(
                    device=device,
                    content_type=config.get("content_type"),
                    content_path=config.get("content_path"),
                    caption=config.get("caption"),
                    **config.get("options", {})
                )
                return StepResult(
                    success=result.get("success", False),
                    data=result,
                    error=result.get("error")
                )

            elif action == "custom":
                # Custom action with arbitrary method call
                method_name = config.get("method")
                if not method_name or not hasattr(agent, method_name):
                    return StepResult(
                        success=False,
                        error=f"Unknown method: {method_name}"
                    )

                method = getattr(agent, method_name)
                result = await method(device=device, **config.get("params", {}))

                return StepResult(
                    success=result.get("success", False) if isinstance(result, dict) else bool(result),
                    data=result if isinstance(result, dict) else {"result": result},
                    error=result.get("error") if isinstance(result, dict) else None
                )

            else:
                return StepResult(
                    success=False,
                    error=f"Unknown action: {action}"
                )

        except Exception as e:
            logger.error(f"Error dispatching to agent: {e}")
            return StepResult(success=False, error=str(e))

    async def _check_step_condition(
        self,
        step,
        previous_results: List[Dict]
    ) -> bool:
        """Check if step condition is met"""
        if not step.condition:
            return True

        condition = step.condition

        # Check previous step success
        if "previous_step" in condition:
            expected = condition["previous_step"]
            if previous_results:
                last_result = previous_results[-1]["result"]
                if expected == "success" and not last_result.success:
                    return False
                if expected == "failure" and last_result.success:
                    return False

        # Check specific step result
        if "step_id" in condition:
            step_id = condition["step_id"]
            expected_result = condition.get("result", "success")

            for r in previous_results:
                if r["step_id"] == step_id:
                    if expected_result == "success" and not r["result"].success:
                        return False
                    if expected_result == "failure" and r["result"].success:
                        return False
                    break

        return True

    async def _interruptible_sleep(self, scenario_id: str, seconds: float) -> None:
        """Sleep that can be interrupted by pause/cancel"""
        end_time = asyncio.get_event_loop().time() + seconds

        while asyncio.get_event_loop().time() < end_time:
            # Check for cancellation
            if self._cancel_flags.get(scenario_id):
                return

            # Check for pause
            if self._scenario_states.get(scenario_id) == ScenarioState.PAUSED:
                await self._pause_events[scenario_id].wait()

            await asyncio.sleep(min(1.0, end_time - asyncio.get_event_loop().time()))

    async def _load_scenario(self, scenario_id: str):
        """Load scenario from database"""
        if not self._get_db:
            logger.error("Database not configured")
            return None

        try:
            from ..database.db import SessionLocal
            from ..database import models

            db = SessionLocal()
            try:
                scenario = db.query(models.Scenario).filter(
                    models.Scenario.id == scenario_id
                ).first()

                if scenario:
                    # Eagerly load steps
                    _ = scenario.steps

                return scenario
            finally:
                db.close()

        except Exception as e:
            logger.error(f"Error loading scenario: {e}")
            return None

    async def _get_device(self, device_id: Optional[str]):
        """Get device from device manager"""
        if not device_id or not self._device_manager:
            return None

        return self._device_manager.devices.get(device_id)

    async def _update_scenario_status(
        self,
        scenario_id: str,
        status: str,
        error_message: Optional[str] = None
    ) -> None:
        """Update scenario status in database"""
        if not self._get_db:
            return

        try:
            from ..database.db import SessionLocal
            from ..database import models

            db = SessionLocal()
            try:
                scenario = db.query(models.Scenario).filter(
                    models.Scenario.id == scenario_id
                ).first()

                if scenario:
                    scenario.status = status
                    scenario.updated_at = datetime.utcnow()

                    if status == "running":
                        scenario.started_at = datetime.utcnow()
                    elif status in ("completed", "failed", "cancelled"):
                        scenario.completed_at = datetime.utcnow()
                        scenario.last_run_at = datetime.utcnow()

                    if error_message:
                        scenario.error_message = error_message

                    db.commit()
            finally:
                db.close()

        except Exception as e:
            logger.error(f"Error updating scenario status: {e}")

    async def _update_scenario_progress(
        self,
        scenario_id: str,
        current_step: int,
        total_steps: int
    ) -> None:
        """Update scenario progress in database"""
        if not self._get_db:
            return

        try:
            from ..database.db import SessionLocal
            from ..database import models

            db = SessionLocal()
            try:
                scenario = db.query(models.Scenario).filter(
                    models.Scenario.id == scenario_id
                ).first()

                if scenario:
                    scenario.current_step_index = current_step
                    scenario.total_steps = total_steps
                    scenario.updated_at = datetime.utcnow()
                    db.commit()
            finally:
                db.close()

        except Exception as e:
            logger.error(f"Error updating scenario progress: {e}")

    async def _update_step_status(
        self,
        step_id: str,
        status: str,
        result: Optional[Dict] = None,
        error_message: Optional[str] = None
    ) -> None:
        """Update step status in database"""
        if not self._get_db:
            return

        try:
            from ..database.db import SessionLocal
            from ..database import models

            db = SessionLocal()
            try:
                step = db.query(models.ScenarioStep).filter(
                    models.ScenarioStep.id == step_id
                ).first()

                if step:
                    step.status = status

                    if status == "running":
                        step.started_at = datetime.utcnow()
                        step.attempt_count += 1
                    elif status in ("completed", "failed", "skipped"):
                        step.completed_at = datetime.utcnow()

                    if result:
                        step.result = result
                    if error_message:
                        step.error_message = error_message

                    db.commit()
            finally:
                db.close()

        except Exception as e:
            logger.error(f"Error updating step status: {e}")

    async def _notify_scenario_update(
        self,
        event_type: str,
        scenario_id: str,
        data: Dict[str, Any]
    ) -> None:
        """Send WebSocket notification about scenario update"""
        if not self._ws_manager:
            return

        try:
            await self._ws_manager.broadcast({
                "type": f"scenario_{event_type}",
                "scenario_id": scenario_id,
                "data": data,
                "timestamp": datetime.utcnow().isoformat(),
            })
        except Exception as e:
            logger.error(f"Failed to send scenario notification: {e}")


# Global instance
scenario_runner = ScenarioRunner()
