"""Workflows API Routes - CRUD and execution endpoints for visual workflows"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from loguru import logger

from ..database.db import get_db
from ..database import models, schemas


router = APIRouter(prefix="/api/workflows", tags=["workflows"])


# ============================================
# WORKFLOW CRUD ENDPOINTS
# ============================================

@router.get(
    "/",
    summary="List all workflows",
    description="Get a list of all visual workflows with optional filtering"
)
async def list_workflows(
    status: Optional[str] = None,
    device_id: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    List all workflows with optional filtering.

    **Args:**
    - **status**: Filter by workflow status (draft, active, running, etc.)
    - **device_id**: Filter by assigned device
    - **limit**: Maximum results (default: 50, max: 200)
    - **offset**: Pagination offset

    **Returns:**
    List of workflows (without node/edge details for performance)
    """
    try:
        query = db.query(models.Workflow)

        if status:
            query = query.filter(models.Workflow.status == status)
        if device_id:
            query = query.filter(models.Workflow.device_id == device_id)

        workflows = query.order_by(
            models.Workflow.updated_at.desc()
        ).offset(offset).limit(min(limit, 200)).all()

        # Build response with node count
        result = []
        for wf in workflows:
            result.append({
                "id": wf.id,
                "name": wf.name,
                "description": wf.description,
                "status": wf.status,
                "device_id": wf.device_id,
                "run_count": wf.run_count,
                "success_count": wf.success_count,
                "failure_count": wf.failure_count,
                "node_count": len(wf.nodes),
                "last_run_at": wf.last_run_at,
                "created_at": wf.created_at,
                "updated_at": wf.updated_at,
            })

        logger.info(f"Listed {len(result)} workflows")
        return {"workflows": result, "total": len(result)}

    except Exception as e:
        logger.error(f"Error listing workflows: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/",
    status_code=201,
    summary="Create a new workflow",
    description="Create a new visual workflow with nodes and edges"
)
async def create_workflow(
    workflow_data: schemas.WorkflowCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new workflow with nodes and edges.

    **Args:**
    - **workflow_data**: Workflow configuration including name, description, nodes, edges

    **Returns:**
    Created workflow with generated ID
    """
    try:
        # Create workflow
        workflow = models.Workflow(
            id=str(uuid.uuid4()),
            name=workflow_data.name,
            description=workflow_data.description,
            device_id=workflow_data.device_id,
            status=models.WorkflowStatus.DRAFT.value,
        )

        db.add(workflow)

        # Create nodes
        for node_data in workflow_data.nodes:
            node = models.WorkflowNode(
                id=node_data.id,
                workflow_id=workflow.id,
                node_type=node_data.type,
                position_x=node_data.position.get("x", 0),
                position_y=node_data.position.get("y", 0),
                data=node_data.data,
            )
            db.add(node)

        # Create edges
        for edge_data in workflow_data.edges:
            edge = models.WorkflowEdge(
                id=edge_data.id,
                workflow_id=workflow.id,
                source_node_id=edge_data.source,
                target_node_id=edge_data.target,
                source_handle=edge_data.sourceHandle,
                target_handle=edge_data.targetHandle,
                label=edge_data.label,
                animated=edge_data.animated,
                style=edge_data.style,
            )
            db.add(edge)

        db.commit()
        db.refresh(workflow)

        logger.success(f"Created workflow: {workflow.name} (id: {workflow.id})")

        # Build response
        return _workflow_to_response(workflow)

    except Exception as e:
        db.rollback()
        logger.error(f"Error creating workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{workflow_id}",
    summary="Get workflow details",
    description="Get detailed information about a workflow including all nodes and edges"
)
async def get_workflow(
    workflow_id: str,
    db: Session = Depends(get_db)
):
    """
    Get workflow details by ID.

    **Args:**
    - **workflow_id**: Unique workflow identifier

    **Returns:**
    Workflow with all nodes and edges (ReactFlow format)
    """
    workflow = db.query(models.Workflow).filter(
        models.Workflow.id == workflow_id
    ).first()

    if not workflow:
        raise HTTPException(status_code=404, detail=f"Workflow not found: {workflow_id}")

    return _workflow_to_response(workflow)


@router.put(
    "/{workflow_id}",
    summary="Update workflow",
    description="Update workflow configuration including nodes and edges"
)
async def update_workflow(
    workflow_id: str,
    update_data: schemas.WorkflowUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a workflow.

    **Args:**
    - **workflow_id**: Workflow ID to update
    - **update_data**: Fields to update (partial update supported)

    **Returns:**
    Updated workflow

    **Note:** Cannot update a running workflow
    """
    workflow = db.query(models.Workflow).filter(
        models.Workflow.id == workflow_id
    ).first()

    if not workflow:
        raise HTTPException(status_code=404, detail=f"Workflow not found: {workflow_id}")

    if workflow.status == models.WorkflowStatus.RUNNING.value:
        raise HTTPException(status_code=400, detail="Cannot update a running workflow")

    try:
        # Update basic fields
        if update_data.name is not None:
            workflow.name = update_data.name
        if update_data.description is not None:
            workflow.description = update_data.description
        if update_data.device_id is not None:
            workflow.device_id = update_data.device_id

        # Update nodes if provided (replace all)
        if update_data.nodes is not None:
            # Delete existing nodes
            db.query(models.WorkflowNode).filter(
                models.WorkflowNode.workflow_id == workflow_id
            ).delete()

            # Add new nodes
            for node_data in update_data.nodes:
                node = models.WorkflowNode(
                    id=node_data.id,
                    workflow_id=workflow_id,
                    node_type=node_data.type,
                    position_x=node_data.position.get("x", 0),
                    position_y=node_data.position.get("y", 0),
                    data=node_data.data,
                )
                db.add(node)

        # Update edges if provided (replace all)
        if update_data.edges is not None:
            # Delete existing edges
            db.query(models.WorkflowEdge).filter(
                models.WorkflowEdge.workflow_id == workflow_id
            ).delete()

            # Add new edges
            for edge_data in update_data.edges:
                edge = models.WorkflowEdge(
                    id=edge_data.id,
                    workflow_id=workflow_id,
                    source_node_id=edge_data.source,
                    target_node_id=edge_data.target,
                    source_handle=edge_data.sourceHandle,
                    target_handle=edge_data.targetHandle,
                    label=edge_data.label,
                    animated=edge_data.animated,
                    style=edge_data.style,
                )
                db.add(edge)

        workflow.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(workflow)

        logger.success(f"Updated workflow: {workflow_id}")
        return _workflow_to_response(workflow)

    except Exception as e:
        db.rollback()
        logger.error(f"Error updating workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/{workflow_id}",
    summary="Delete workflow",
    description="Delete a workflow and all its nodes/edges"
)
async def delete_workflow(
    workflow_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a workflow.

    **Args:**
    - **workflow_id**: Workflow ID to delete

    **Returns:**
    Success confirmation

    **Warning:** This action is permanent. Cannot delete a running workflow.
    """
    workflow = db.query(models.Workflow).filter(
        models.Workflow.id == workflow_id
    ).first()

    if not workflow:
        raise HTTPException(status_code=404, detail=f"Workflow not found: {workflow_id}")

    if workflow.status == models.WorkflowStatus.RUNNING.value:
        raise HTTPException(status_code=400, detail="Cannot delete a running workflow")

    try:
        db.delete(workflow)  # Cascades to nodes and edges
        db.commit()

        logger.success(f"Deleted workflow: {workflow_id}")
        return {"success": True, "message": f"Workflow {workflow_id} deleted"}

    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# WORKFLOW EXECUTION ENDPOINTS
# ============================================

@router.post(
    "/{workflow_id}/run",
    summary="Run workflow",
    description="Start executing a workflow"
)
async def run_workflow(
    workflow_id: str,
    run_request: schemas.WorkflowRunRequest = None,
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Start executing a workflow.

    **Args:**
    - **workflow_id**: Workflow to run
    - **device_id** (optional): Override default device
    - **dry_run** (optional): Test mode without actual execution

    **Returns:**
    Execution status

    **Real-time Updates:**
    Progress is broadcasted via WebSocket events:
    - workflow_started
    - node_executed
    - workflow_completed
    """
    workflow = db.query(models.Workflow).filter(
        models.Workflow.id == workflow_id
    ).first()

    if not workflow:
        raise HTTPException(status_code=404, detail=f"Workflow not found: {workflow_id}")

    if workflow.status == models.WorkflowStatus.RUNNING.value:
        raise HTTPException(status_code=400, detail="Workflow is already running")

    if not workflow.nodes:
        raise HTTPException(status_code=400, detail="Workflow has no nodes")

    request = run_request or schemas.WorkflowRunRequest()

    try:
        # Import here to avoid circular imports
        from ..orchestration.workflow_executor import workflow_executor

        # Run in background
        if background_tasks:
            background_tasks.add_task(
                workflow_executor.execute_workflow,
                workflow_id=workflow_id,
                device_id=request.device_id,
                dry_run=request.dry_run
            )

            logger.info(f"Started workflow (background): {workflow_id}")
            return {
                "success": True,
                "message": "Workflow started",
                "workflow_id": workflow_id,
                "dry_run": request.dry_run,
            }

        # Run synchronously (for testing)
        result = await workflow_executor.execute_workflow(
            workflow_id=workflow_id,
            device_id=request.device_id,
            dry_run=request.dry_run
        )

        return result

    except ImportError:
        # Workflow executor not implemented yet
        logger.warning("Workflow executor not implemented, returning mock response")
        return {
            "success": True,
            "message": "Workflow execution not yet implemented",
            "workflow_id": workflow_id,
            "dry_run": request.dry_run if request else False,
        }

    except Exception as e:
        logger.error(f"Error starting workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/{workflow_id}/duplicate",
    status_code=201,
    summary="Duplicate workflow",
    description="Create a copy of an existing workflow"
)
async def duplicate_workflow(
    workflow_id: str,
    db: Session = Depends(get_db)
):
    """
    Create a copy of an existing workflow.

    **Args:**
    - **workflow_id**: Workflow to duplicate

    **Returns:**
    New workflow (copy)
    """
    workflow = db.query(models.Workflow).filter(
        models.Workflow.id == workflow_id
    ).first()

    if not workflow:
        raise HTTPException(status_code=404, detail=f"Workflow not found: {workflow_id}")

    try:
        # Create new workflow
        new_workflow = models.Workflow(
            id=str(uuid.uuid4()),
            name=f"{workflow.name} (copy)",
            description=workflow.description,
            device_id=workflow.device_id,
            status=models.WorkflowStatus.DRAFT.value,
        )
        db.add(new_workflow)

        # Map old node IDs to new node IDs
        node_id_map = {}

        # Copy nodes with new IDs
        for node in workflow.nodes:
            new_node_id = f"{node.id}-{str(uuid.uuid4())[:8]}"
            node_id_map[node.id] = new_node_id

            new_node = models.WorkflowNode(
                id=new_node_id,
                workflow_id=new_workflow.id,
                node_type=node.node_type,
                position_x=node.position_x,
                position_y=node.position_y,
                data=node.data,
            )
            db.add(new_node)

        # Copy edges with updated node references
        for edge in workflow.edges:
            new_edge = models.WorkflowEdge(
                id=f"{edge.id}-{str(uuid.uuid4())[:8]}",
                workflow_id=new_workflow.id,
                source_node_id=node_id_map.get(edge.source_node_id, edge.source_node_id),
                target_node_id=node_id_map.get(edge.target_node_id, edge.target_node_id),
                source_handle=edge.source_handle,
                target_handle=edge.target_handle,
                label=edge.label,
                animated=edge.animated,
                style=edge.style,
            )
            db.add(new_edge)

        db.commit()
        db.refresh(new_workflow)

        logger.success(f"Duplicated workflow: {workflow_id} -> {new_workflow.id}")
        return _workflow_to_response(new_workflow)

    except Exception as e:
        db.rollback()
        logger.error(f"Error duplicating workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# HELPER FUNCTIONS
# ============================================

def _workflow_to_response(workflow: models.Workflow) -> dict:
    """Convert workflow ORM model to API response format (ReactFlow compatible)"""
    nodes = [
        {
            "id": node.id,
            "type": node.node_type,
            "position": {"x": node.position_x, "y": node.position_y},
            "data": node.data or {},
        }
        for node in workflow.nodes
    ]

    edges = [
        {
            "id": edge.id,
            "source": edge.source_node_id,
            "target": edge.target_node_id,
            "sourceHandle": edge.source_handle,
            "targetHandle": edge.target_handle,
            "label": edge.label,
            "animated": edge.animated or False,
            "style": edge.style,
        }
        for edge in workflow.edges
    ]

    return {
        "id": workflow.id,
        "name": workflow.name,
        "description": workflow.description,
        "status": workflow.status,
        "device_id": workflow.device_id,
        "run_count": workflow.run_count,
        "success_count": workflow.success_count,
        "failure_count": workflow.failure_count,
        "last_run_at": workflow.last_run_at,
        "created_at": workflow.created_at,
        "updated_at": workflow.updated_at,
        "nodes": nodes,
        "edges": edges,
    }
