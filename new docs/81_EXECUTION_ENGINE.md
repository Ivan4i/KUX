# 81_EXECUTION_ENGINE.md

## Workflow Execution Engine

### Core Execution Flow

```
Workflow Execution Pipeline:

User triggers workflow
    ↓
Create Task in database
    ↓
Add to execution queue
    ↓
Pick available device
    ↓
Execute workflow nodes (sequential)
    ├─ Start node
    ├─ Action nodes (click, type, wait, etc)
    ├─ Condition nodes (if/else)
    └─ End node
    ↓
Collect results
    ↓
Update task status
    ↓
Send notifications (WebSocket)
    ↓
Store analytics
```

### ExecutionEngine Class

```python
# app/core/execution_engine.py
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

from app.models.task import Task, TaskStatus
from app.models.device import Device
from app.schemas.workflow import Workflow, WorkflowNode, WorkflowEdge
from app.services.notification_service import NotificationService
from app.services.adb_service import ADBService
from app.services.alignui_service import AlignUIService

logger = logging.getLogger(__name__)

class NodeType(str, Enum):
    START = "start"
    END = "end"
    ACTION = "action"
    CONDITION = "condition"
    DELAY = "delay"

class ExecutionEngine:
    """
    Execute workflows on Android devices.
    
    Responsibilities:
    - Parse workflow structure
    - Execute nodes sequentially
    - Handle conditions and branching
    - Capture results and errors
    - Send real-time notifications
    """
    
    def __init__(
        self,
        notification_service: NotificationService,
        adb_service: ADBService,
        alignui_service: AlignUIService,
    ):
        self.notification_service = notification_service
        self.adb = adb_service
        self.alignui = alignui_service
        self.execution_context = {}
    
    async def execute_workflow(
        self,
        workflow: Workflow,
        device: Device,
        task: Task,
    ) -> Dict[str, Any]:
        """
        Execute workflow on device.
        
        Returns:
            {
                "success": bool,
                "task_id": str,
                "device_id": str,
                "duration_seconds": float,
                "nodes_executed": int,
                "errors": List[str],
                "results": Dict
            }
        """
        
        start_time = datetime.now()
        logger.info(f"🚀 Starting workflow: {workflow.id} on {device.id}")
        
        try:
            # Initialize execution context
            self.execution_context = {
                "workflow_id": workflow.id,
                "device_id": device.id,
                "task_id": task.id,
                "start_time": start_time,
                "variables": {},
                "node_results": {},
                "errors": [],
            }
            
            # Update task status
            task.status = TaskStatus.RUNNING
            await task.save()
            
            # Find start node
            start_node = next(
                (n for n in workflow.nodes if n.type == NodeType.START),
                None
            )
            
            if not start_node:
                raise ValueError("Workflow must have a start node")
            
            # Execute from start node
            current_node_id = start_node.id
            nodes_executed = 0
            max_nodes = len(workflow.nodes) * 2  # Prevent infinite loops
            
            while current_node_id and nodes_executed < max_nodes:
                nodes_executed += 1
                
                # Get current node
                current_node = next(
                    (n for n in workflow.nodes if n.id == current_node_id),
                    None
                )
                
                if not current_node:
                    logger.error(f"Node not found: {current_node_id}")
                    break
                
                # Execute node
                logger.info(f"  → Executing node: {current_node.label} ({current_node.type})")
                
                try:
                    result = await self.execute_node(current_node, device, workflow)
                    
                    # Store result
                    self.execution_context["node_results"][current_node_id] = result
                    
                    # Send progress notification
                    await self.notification_service.notify_progress(
                        device.id,
                        current_node.label,
                        nodes_executed,
                        len(workflow.nodes)
                    )
                
                except Exception as e:
                    error_msg = f"Node failed: {current_node.label} - {str(e)}"
                    logger.error(error_msg)
                    self.execution_context["errors"].append(error_msg)
                    
                    # Stop on error (unless configured otherwise)
                    if current_node.data.get("stop_on_error", True):
                        break
                
                # Find next node
                if current_node.type == NodeType.END:
                    logger.info("✅ Workflow completed")
                    break
                
                # Get edge from current node
                edge = next(
                    (e for e in workflow.edges if e.source == current_node_id),
                    None
                )
                
                if edge:
                    current_node_id = edge.target
                else:
                    logger.warning(f"No edge from {current_node_id}")
                    break
            
            # Calculate duration
            duration = (datetime.now() - start_time).total_seconds()
            
            # Prepare result
            success = len(self.execution_context["errors"]) == 0
            result = {
                "success": success,
                "task_id": task.id,
                "device_id": device.id,
                "duration_seconds": duration,
                "nodes_executed": nodes_executed,
                "errors": self.execution_context["errors"],
                "results": self.execution_context["node_results"],
            }
            
            # Update task
            task.status = TaskStatus.COMPLETED if success else TaskStatus.FAILED
            task.duration_seconds = duration
            task.error_message = "; ".join(self.execution_context["errors"]) if self.execution_context["errors"] else None
            await task.save()
            
            # Send completion notification
            await self.notification_service.notify_completion(
                device.id,
                task.id,
                success
            )
            
            logger.info(f"✅ Workflow completed in {duration:.2f}s - Success: {success}")
            return result
        
        except Exception as e:
            logger.error(f"❌ Workflow execution failed: {e}")
            
            # Update task with error
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            await task.save()
            
            return {
                "success": False,
                "task_id": task.id,
                "device_id": device.id,
                "errors": [str(e)],
                "results": {},
            }
    
    async def execute_node(
        self,
        node: WorkflowNode,
        device: Device,
        workflow: Workflow,
    ) -> Dict[str, Any]:
        """Execute individual workflow node."""
        
        if node.type == NodeType.START:
            return {"type": "start", "status": "success"}
        
        elif node.type == NodeType.END:
            return {"type": "end", "status": "success"}
        
        elif node.type == NodeType.DELAY:
            return await self.execute_delay(node)
        
        elif node.type == NodeType.ACTION:
            return await self.execute_action(node, device)
        
        elif node.type == NodeType.CONDITION:
            return await self.execute_condition(node, device, workflow)
        
        else:
            raise ValueError(f"Unknown node type: {node.type}")
    
    async def execute_delay(self, node: WorkflowNode) -> Dict[str, Any]:
        """Execute delay/wait node."""
        
        duration = node.data.get("duration", 1000)  # milliseconds
        
        logger.info(f"⏸️  Waiting {duration}ms")
        await asyncio.sleep(duration / 1000)
        
        return {"type": "delay", "duration_ms": duration, "status": "success"}
    
    async def execute_action(
        self,
        node: WorkflowNode,
        device: Device,
    ) -> Dict[str, Any]:
        """Execute action node (click, type, etc)."""
        
        action_type = node.data.get("action_type")
        params = node.data.get("params", {})
        
        if action_type == "click":
            return await self.action_click(device, params)
        
        elif action_type == "type":
            return await self.action_type(device, params)
        
        elif action_type == "open_app":
            return await self.action_open_app(device, params)
        
        elif action_type == "back":
            return await self.adb.press_back(device.id)
        
        elif action_type == "home":
            return await self.adb.press_home(device.id)
        
        elif action_type == "screenshot":
            return await self.action_screenshot(device, params)
        
        else:
            raise ValueError(f"Unknown action: {action_type}")
    
    async def action_click(self, device: Device, params: Dict) -> Dict:
        """Click on element by label or coordinates."""
        
        if "label" in params:
            # Find element by label using AlignUI
            screenshot_path = await self.adb.take_screenshot(device.id)
            element = await self.alignui.find_element(screenshot_path, params["label"])
            
            if not element:
                raise ValueError(f"Element not found: {params['label']}")
            
            # Click element
            await self.alignui.click_element(device.id, element)
            
            return {
                "type": "click",
                "label": params["label"],
                "coordinates": {
                    "x": element.coordinates.x,
                    "y": element.coordinates.y,
                },
                "status": "success",
            }
        
        elif "x" in params and "y" in params:
            # Click on specific coordinates
            x = params["x"]
            y = params["y"]
            
            await self.adb.click(device.id, x, y)
            
            return {
                "type": "click",
                "coordinates": {"x": x, "y": y},
                "status": "success",
            }
        
        else:
            raise ValueError("Click requires either 'label' or 'x'/'y' coordinates")
    
    async def action_type(self, device: Device, params: Dict) -> Dict:
        """Type text on device."""
        
        text = params.get("text", "")
        
        if not text:
            raise ValueError("Type action requires 'text' parameter")
        
        await self.adb.type_text(device.id, text)
        
        return {
            "type": "type",
            "text": text[:50] + "..." if len(text) > 50 else text,
            "status": "success",
        }
    
    async def action_open_app(self, device: Device, params: Dict) -> Dict:
        """Open application."""
        
        package = params.get("package")
        activity = params.get("activity", "MainActivity")
        
        if not package:
            raise ValueError("open_app requires 'package' parameter")
        
        await self.adb.open_app(device.id, package, activity)
        
        return {
            "type": "open_app",
            "package": package,
            "activity": activity,
            "status": "success",
        }
    
    async def action_screenshot(self, device: Device, params: Dict) -> Dict:
        """Take screenshot."""
        
        path = await self.adb.take_screenshot(device.id)
        
        # Extract text if requested
        text = None
        if params.get("extract_text"):
            text = await self.alignui.extract_text(path)
        
        return {
            "type": "screenshot",
            "path": path,
            "text": text,
            "status": "success",
        }
    
    async def execute_condition(
        self,
        node: WorkflowNode,
        device: Device,
        workflow: Workflow,
    ) -> Dict[str, Any]:
        """
        Execute condition node.
        
        Modifies execution flow based on condition result.
        """
        
        condition_type = node.data.get("condition_type")
        params = node.data.get("params", {})
        
        # Evaluate condition
        if condition_type == "element_exists":
            # Check if element exists on screen
            screenshot_path = await self.adb.take_screenshot(device.id)
            element = await self.alignui.find_element(screenshot_path, params["label"])
            result = element is not None
        
        elif condition_type == "text_contains":
            # Check if screen contains text
            screenshot_path = await self.adb.take_screenshot(device.id)
            text = await self.alignui.extract_text(screenshot_path)
            result = params["text"] in text
        
        else:
            raise ValueError(f"Unknown condition: {condition_type}")
        
        # Update execution flow based on result
        # (This is handled by the workflow edges: true/false branches)
        
        return {
            "type": "condition",
            "condition": condition_type,
            "result": result,
            "status": "success",
        }
```

---

## End of 81_EXECUTION_ENGINE.md