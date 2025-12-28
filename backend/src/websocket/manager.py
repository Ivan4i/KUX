"""WebSocket Manager - handles real-time updates to frontend"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict, Any
from datetime import datetime
import json
import asyncio
from loguru import logger


class WebSocketManager:
    """Manages WebSocket connections and broadcasts"""

    def __init__(self):
        """Initialize WebSocket Manager"""
        self.active_connections: List[WebSocket] = []
        self.connection_ids: Dict[WebSocket, str] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()

    async def connect(self, websocket: WebSocket, client_id: str = None):
        """
        Accept new WebSocket connection

        Args:
            websocket: WebSocket instance
            client_id: Optional client identifier
        """
        await websocket.accept()
        self.active_connections.append(websocket)

        client_id = client_id or f"client_{len(self.active_connections)}"
        self.connection_ids[websocket] = client_id

        logger.info(f"🔌 WebSocket connected: {client_id} (total: {len(self.active_connections)})")

        # Send welcome message
        await self.send_personal_message({
            "type": "connection_established",
            "client_id": client_id,
            "timestamp": datetime.utcnow().isoformat()
        }, websocket)

    def disconnect(self, websocket: WebSocket):
        """
        Remove WebSocket connection

        Args:
            websocket: WebSocket instance
        """
        if websocket in self.active_connections:
            client_id = self.connection_ids.get(websocket, "unknown")
            self.active_connections.remove(websocket)
            del self.connection_ids[websocket]

            logger.info(f"🔌 WebSocket disconnected: {client_id} (total: {len(self.active_connections)})")

    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """
        Send message to specific client

        Args:
            message: Message data
            websocket: WebSocket instance
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")

    async def broadcast(self, message: Dict[str, Any]):
        """
        Broadcast message to all connected clients

        Args:
            message: Message data
        """
        if not self.active_connections:
            return

        # Add timestamp if not present
        if "timestamp" not in message:
            message["timestamp"] = datetime.utcnow().isoformat()

        logger.debug(f"📡 Broadcasting: {message.get('type')} to {len(self.active_connections)} clients")

        # Send to all connections
        disconnected = []

        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                disconnected.append(connection)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.append(connection)

        # Remove disconnected clients
        for connection in disconnected:
            self.disconnect(connection)

    # Event-specific broadcast methods

    async def broadcast_device_status_update(
        self,
        device_id: str,
        status_data: Dict[str, Any]
    ):
        """
        Broadcast device status update

        Args:
            device_id: Device ID
            status_data: Device status data
        """
        await self.broadcast({
            "type": "device_status_update",
            "device_id": device_id,
            "data": status_data
        })

    async def broadcast_task_started(
        self,
        task_id: int,
        task_data: Dict[str, Any]
    ):
        """
        Broadcast task started event

        Args:
            task_id: Task ID
            task_data: Task data
        """
        await self.broadcast({
            "type": "task_started",
            "task_id": task_id,
            "data": task_data
        })

    async def broadcast_task_progress(
        self,
        task_id: int,
        progress_message: str,
        progress_percent: int = None
    ):
        """
        Broadcast task progress update

        Args:
            task_id: Task ID
            progress_message: Progress message (e.g., "Opening WhatsApp...")
            progress_percent: Optional progress percentage (0-100)
        """
        await self.broadcast({
            "type": "task_progress",
            "task_id": task_id,
            "message": progress_message,
            "progress_percent": progress_percent
        })

    async def broadcast_task_completed(
        self,
        task_id: int,
        result_data: Dict[str, Any]
    ):
        """
        Broadcast task completed event

        Args:
            task_id: Task ID
            result_data: Task result data
        """
        await self.broadcast({
            "type": "task_completed",
            "task_id": task_id,
            "data": result_data
        })

    async def broadcast_task_failed(
        self,
        task_id: int,
        error_message: str,
        error_data: Dict[str, Any] = None
    ):
        """
        Broadcast task failed event

        Args:
            task_id: Task ID
            error_message: Error message
            error_data: Optional error data
        """
        await self.broadcast({
            "type": "task_failed",
            "task_id": task_id,
            "error": error_message,
            "data": error_data or {}
        })

    async def broadcast_log_entry(
        self,
        log_data: Dict[str, Any]
    ):
        """
        Broadcast new log entry

        Args:
            log_data: Log entry data
        """
        await self.broadcast({
            "type": "log_entry",
            "data": log_data
        })

    async def broadcast_notification(
        self,
        level: str,
        message: str,
        data: Dict[str, Any] = None
    ):
        """
        Broadcast notification to all clients

        Args:
            level: Notification level (info, warning, error, success)
            message: Notification message
            data: Optional additional data
        """
        await self.broadcast({
            "type": "notification",
            "level": level,
            "message": message,
            "data": data or {}
        })

    # Scenario-specific broadcast methods

    async def broadcast_scenario_started(
        self,
        scenario_id: str,
        scenario_data: Dict[str, Any]
    ):
        """
        Broadcast scenario started event

        Args:
            scenario_id: Scenario ID
            scenario_data: Scenario data (device_id, total_steps, etc.)
        """
        await self.broadcast({
            "type": "scenario_started",
            "scenario_id": scenario_id,
            "data": scenario_data
        })

    async def broadcast_scenario_progress(
        self,
        scenario_id: str,
        current_step: int,
        total_steps: int,
        step_name: str = None
    ):
        """
        Broadcast scenario progress update

        Args:
            scenario_id: Scenario ID
            current_step: Current step number
            total_steps: Total number of steps
            step_name: Name of current step
        """
        await self.broadcast({
            "type": "scenario_progress",
            "scenario_id": scenario_id,
            "current_step": current_step,
            "total_steps": total_steps,
            "step_name": step_name,
            "progress_percent": int((current_step / total_steps) * 100) if total_steps > 0 else 0
        })

    async def broadcast_scenario_step_completed(
        self,
        scenario_id: str,
        step_data: Dict[str, Any]
    ):
        """
        Broadcast scenario step completed event

        Args:
            scenario_id: Scenario ID
            step_data: Step data (step_id, step_name, result)
        """
        await self.broadcast({
            "type": "scenario_step_completed",
            "scenario_id": scenario_id,
            "data": step_data
        })

    async def broadcast_scenario_step_failed(
        self,
        scenario_id: str,
        step_data: Dict[str, Any]
    ):
        """
        Broadcast scenario step failed event

        Args:
            scenario_id: Scenario ID
            step_data: Step data (step_id, step_name, error)
        """
        await self.broadcast({
            "type": "scenario_step_failed",
            "scenario_id": scenario_id,
            "data": step_data
        })

    async def broadcast_scenario_completed(
        self,
        scenario_id: str,
        result_data: Dict[str, Any]
    ):
        """
        Broadcast scenario completed event

        Args:
            scenario_id: Scenario ID
            result_data: Completion data (success_count, failure_count, etc.)
        """
        await self.broadcast({
            "type": "scenario_completed",
            "scenario_id": scenario_id,
            "data": result_data
        })

    async def broadcast_scenario_failed(
        self,
        scenario_id: str,
        error_message: str,
        error_data: Dict[str, Any] = None
    ):
        """
        Broadcast scenario failed event

        Args:
            scenario_id: Scenario ID
            error_message: Error message
            error_data: Additional error data
        """
        await self.broadcast({
            "type": "scenario_failed",
            "scenario_id": scenario_id,
            "error": error_message,
            "data": error_data or {}
        })

    async def broadcast_scenario_paused(self, scenario_id: str):
        """Broadcast scenario paused event"""
        await self.broadcast({
            "type": "scenario_paused",
            "scenario_id": scenario_id
        })

    async def broadcast_scenario_resumed(self, scenario_id: str):
        """Broadcast scenario resumed event"""
        await self.broadcast({
            "type": "scenario_resumed",
            "scenario_id": scenario_id
        })

    async def broadcast_scenario_cancelled(self, scenario_id: str):
        """Broadcast scenario cancelled event"""
        await self.broadcast({
            "type": "scenario_cancelled",
            "scenario_id": scenario_id
        })

    # Queue status broadcasts

    async def broadcast_queue_status(self, queue_data: Dict[str, Any]):
        """
        Broadcast queue status update

        Args:
            queue_data: Queue status data
        """
        await self.broadcast({
            "type": "queue_status",
            "data": queue_data
        })

    async def handle_client_message(self, message: Dict[str, Any], websocket: WebSocket):
        """
        Handle incoming message from client

        Args:
            message: Message from client
            websocket: Client WebSocket
        """
        message_type = message.get("type")

        logger.debug(f"📨 Received message from client: {message_type}")

        # Handle different message types
        if message_type == "ping":
            await self.send_personal_message({
                "type": "pong",
                "timestamp": datetime.utcnow().isoformat()
            }, websocket)

        elif message_type == "subscribe":
            # Client subscribes to specific events
            # (For MVP, all clients receive all events)
            await self.send_personal_message({
                "type": "subscribed",
                "events": message.get("events", [])
            }, websocket)

        else:
            logger.warning(f"Unknown message type: {message_type}")

    def get_connection_count(self) -> int:
        """Get number of active connections"""
        return len(self.active_connections)

    def get_connection_ids(self) -> List[str]:
        """Get list of connected client IDs"""
        return list(self.connection_ids.values())


# Global WebSocket manager instance
ws_manager = WebSocketManager()
