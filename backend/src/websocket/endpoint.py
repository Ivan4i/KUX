"""WebSocket Endpoint"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from loguru import logger

from .manager import ws_manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time updates

    Clients connect to ws://localhost:8000/ws
    """
    client_id = None

    try:
        # Accept connection
        await ws_manager.connect(websocket)
        client_id = ws_manager.connection_ids.get(websocket)

        logger.info(f"🔌 Client {client_id} connected to WebSocket")

        # Listen for messages
        while True:
            try:
                # Receive message from client
                data = await websocket.receive_json()

                # Handle client message
                await ws_manager.handle_client_message(data, websocket)

            except WebSocketDisconnect:
                logger.info(f"🔌 Client {client_id} disconnected")
                break
            except Exception as e:
                logger.error(f"Error handling WebSocket message: {e}")
                break

    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")

    finally:
        # Clean up connection
        ws_manager.disconnect(websocket)
        logger.info(f"🔌 Client {client_id} connection closed")
