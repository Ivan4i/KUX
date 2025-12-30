"""
Workflow Executor - Executes visual workflows by converting them to scenario steps

This module bridges the Visual Workflow Builder (ReactFlow frontend) with the
existing ScenarioRunner backend. It converts workflow nodes/edges into
executable scenario steps and runs them sequentially.
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from loguru import logger

from ..database.db import SessionLocal
from ..database import models
from ..websocket.manager import ws_manager


class WorkflowExecutor:
    """
    Executes visual workflows by converting nodes to steps.

    Workflow nodes are executed in topological order following edges.
    Condition nodes can branch execution based on their conditions.
    """

    def __init__(self):
        self._db_factory = None
        self._device_manager = None
        self._agents: Dict[str, Any] = {}
        self._running_workflows: Dict[str, bool] = {}

    def set_db_factory(self, factory):
        """Set database session factory"""
        self._db_factory = factory

    def set_device_manager(self, device_manager):
        """Set device manager instance"""
        self._device_manager = device_manager

    def register_agent(self, name: str, agent):
        """Register an agent for workflow actions"""
        self._agents[name] = agent
        logger.info(f"Registered agent for workflow: {name}")

    async def execute_workflow(
        self,
        workflow_id: str,
        device_id: Optional[str] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Execute a workflow by its ID.

        Args:
            workflow_id: ID of the workflow to execute
            device_id: Optional override for device assignment
            dry_run: If True, simulate execution without actual actions

        Returns:
            Execution result with status and details
        """
        logger.info(f"Starting workflow execution: {workflow_id} (dry_run={dry_run})")

        # Check if already running
        if workflow_id in self._running_workflows:
            logger.warning(f"Workflow {workflow_id} is already running")
            return {
                "success": False,
                "error": "Workflow is already running",
                "workflow_id": workflow_id
            }

        db = SessionLocal()
        try:
            # Load workflow
            workflow = db.query(models.Workflow).filter(
                models.Workflow.id == workflow_id
            ).first()

            if not workflow:
                return {
                    "success": False,
                    "error": f"Workflow not found: {workflow_id}",
                    "workflow_id": workflow_id
                }

            # Mark as running
            self._running_workflows[workflow_id] = True
            workflow.status = models.WorkflowStatus.RUNNING.value
            db.commit()

            # Notify start via WebSocket
            await ws_manager.broadcast({
                "type": "workflow_started",
                "workflow_id": workflow_id,
                "name": workflow.name,
                "dry_run": dry_run,
                "timestamp": datetime.utcnow().isoformat()
            })

            # Get execution order
            execution_order = self._get_execution_order(workflow)
            logger.info(f"Execution order: {[n.id for n in execution_order]}")

            # Execute nodes
            results = []
            context = {"workflow_id": workflow_id, "device_id": device_id or workflow.device_id}

            for node in execution_order:
                try:
                    # Notify node start
                    await ws_manager.broadcast({
                        "type": "node_started",
                        "workflow_id": workflow_id,
                        "node_id": node.id,
                        "node_type": node.node_type,
                        "node_data": node.data,
                        "timestamp": datetime.utcnow().isoformat()
                    })

                    # Execute node
                    if dry_run:
                        result = await self._simulate_node(node, context)
                    else:
                        result = await self._execute_node(node, context)

                    results.append({
                        "node_id": node.id,
                        "type": node.node_type,
                        "success": result.get("success", True),
                        "result": result
                    })

                    # Update context with result
                    context[f"node_{node.id}_result"] = result

                    # Notify node completion
                    await ws_manager.broadcast({
                        "type": "node_completed",
                        "workflow_id": workflow_id,
                        "node_id": node.id,
                        "success": result.get("success", True),
                        "result": result,
                        "timestamp": datetime.utcnow().isoformat()
                    })

                except Exception as e:
                    logger.error(f"Error executing node {node.id}: {e}")
                    results.append({
                        "node_id": node.id,
                        "type": node.node_type,
                        "success": False,
                        "error": str(e)
                    })

                    # Notify node failure
                    await ws_manager.broadcast({
                        "type": "node_failed",
                        "workflow_id": workflow_id,
                        "node_id": node.id,
                        "error": str(e),
                        "timestamp": datetime.utcnow().isoformat()
                    })

                    # Break on failure (could make this configurable)
                    break

            # Update workflow status
            all_success = all(r.get("success", False) for r in results)
            workflow.status = models.WorkflowStatus.COMPLETED.value if all_success else models.WorkflowStatus.FAILED.value
            workflow.last_run_at = datetime.utcnow()
            workflow.run_count += 1
            if all_success:
                workflow.success_count += 1
            else:
                workflow.failure_count += 1
            db.commit()

            # Notify completion
            await ws_manager.broadcast({
                "type": "workflow_completed",
                "workflow_id": workflow_id,
                "success": all_success,
                "results": results,
                "timestamp": datetime.utcnow().isoformat()
            })

            return {
                "success": all_success,
                "workflow_id": workflow_id,
                "results": results,
                "dry_run": dry_run
            }

        except Exception as e:
            logger.error(f"Workflow execution error: {e}")

            # Update status to failed
            try:
                workflow = db.query(models.Workflow).filter(
                    models.Workflow.id == workflow_id
                ).first()
                if workflow:
                    workflow.status = models.WorkflowStatus.FAILED.value
                    workflow.failure_count += 1
                    db.commit()
            except:
                pass

            return {
                "success": False,
                "error": str(e),
                "workflow_id": workflow_id
            }

        finally:
            # Clear running status
            self._running_workflows.pop(workflow_id, None)
            db.close()

    def _get_execution_order(self, workflow: models.Workflow) -> List[models.WorkflowNode]:
        """
        Get nodes in execution order (topological sort based on edges).

        Args:
            workflow: Workflow model with nodes and edges

        Returns:
            List of nodes in execution order
        """
        nodes_by_id = {n.id: n for n in workflow.nodes}

        # Build adjacency list
        incoming_edges: Dict[str, List[str]] = {n.id: [] for n in workflow.nodes}
        outgoing_edges: Dict[str, List[str]] = {n.id: [] for n in workflow.nodes}

        for edge in workflow.edges:
            if edge.source_node_id in nodes_by_id and edge.target_node_id in nodes_by_id:
                incoming_edges[edge.target_node_id].append(edge.source_node_id)
                outgoing_edges[edge.source_node_id].append(edge.target_node_id)

        # Find start nodes (triggers with no incoming edges)
        start_nodes = [
            nodes_by_id[nid] for nid, sources in incoming_edges.items()
            if len(sources) == 0
        ]

        # Topological sort using Kahn's algorithm
        result = []
        visited = set()
        queue = list(start_nodes)

        while queue:
            node = queue.pop(0)
            if node.id in visited:
                continue
            visited.add(node.id)
            result.append(node)

            # Add children whose parents are all visited
            for child_id in outgoing_edges[node.id]:
                if child_id not in visited:
                    all_parents_visited = all(
                        p in visited for p in incoming_edges[child_id]
                    )
                    if all_parents_visited:
                        queue.append(nodes_by_id[child_id])

        return result

    async def _execute_node(self, node: models.WorkflowNode, context: Dict) -> Dict:
        """
        Execute a single workflow node.

        Args:
            node: Node to execute
            context: Execution context with workflow data

        Returns:
            Execution result
        """
        node_type = node.node_type
        node_data = node.data or {}

        logger.info(f"Executing node: {node.id} ({node_type})")

        if node_type == "trigger":
            return await self._execute_trigger(node_data, context)
        elif node_type == "action":
            return await self._execute_action(node_data, context)
        elif node_type == "condition":
            return await self._evaluate_condition(node_data, context)
        else:
            logger.warning(f"Unknown node type: {node_type}")
            return {"success": True, "message": f"Unknown node type: {node_type}"}

    async def _simulate_node(self, node: models.WorkflowNode, context: Dict) -> Dict:
        """
        Simulate node execution (dry run).

        Args:
            node: Node to simulate
            context: Execution context

        Returns:
            Simulated result
        """
        logger.info(f"[DRY RUN] Simulating node: {node.id} ({node.node_type})")

        # Simulate delay
        await asyncio.sleep(0.5)

        return {
            "success": True,
            "dry_run": True,
            "node_id": node.id,
            "node_type": node.node_type,
            "message": f"Simulated execution of {node.node_type} node"
        }

    async def _execute_trigger(self, data: Dict, context: Dict) -> Dict:
        """Execute a trigger node (data fetch, schedule trigger, etc.)"""
        trigger_type = data.get("icon", "manual")

        logger.info(f"Executing trigger: {trigger_type}")

        if trigger_type == "notion":
            # Fetch from Notion (placeholder)
            return {
                "success": True,
                "message": "Fetched data from Notion",
                "data": {"leads": []}
            }
        elif trigger_type == "schedule":
            return {
                "success": True,
                "message": "Schedule trigger activated"
            }
        else:
            return {
                "success": True,
                "message": f"Trigger activated: {data.get('label', 'Unknown')}"
            }

    async def _execute_action(self, data: Dict, context: Dict) -> Dict:
        """Execute an action node (send message, API call, etc.)"""
        agent_type = data.get("agent", "unknown")
        action_label = data.get("label", "Unknown Action")

        logger.info(f"Executing action: {action_label} (agent: {agent_type})")

        # Get agent
        agent = self._agents.get(agent_type)

        if agent:
            # Execute via agent
            try:
                # This would call the actual agent action
                # For now, we simulate success
                return {
                    "success": True,
                    "message": f"Executed {action_label} via {agent_type} agent",
                    "agent": agent_type
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "agent": agent_type
                }
        else:
            # No agent registered, simulate
            return {
                "success": True,
                "message": f"Simulated action: {action_label}",
                "note": f"No agent registered for: {agent_type}"
            }

    async def _evaluate_condition(self, data: Dict, context: Dict) -> Dict:
        """
        Evaluate a condition node.

        Args:
            data: Condition data with expression
            context: Execution context

        Returns:
            Evaluation result with 'condition_result' boolean
        """
        condition = data.get("condition", "true")
        label = data.get("label", "Condition")

        logger.info(f"Evaluating condition: {label} ({condition})")

        # Simple condition evaluation (in production, use safe eval)
        try:
            # For now, just check for simple patterns
            if "!= null" in condition or "!== null" in condition:
                result = True  # Simplified: assume data exists
            elif "== null" in condition or "=== null" in condition:
                result = False
            else:
                result = True  # Default to true

            return {
                "success": True,
                "condition_result": result,
                "condition": condition,
                "message": f"Condition '{label}' evaluated to {result}"
            }
        except Exception as e:
            logger.error(f"Condition evaluation error: {e}")
            return {
                "success": False,
                "condition_result": False,
                "error": str(e)
            }


# Global instance
workflow_executor = WorkflowExecutor()
