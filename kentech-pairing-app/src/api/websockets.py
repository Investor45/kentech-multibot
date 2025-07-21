"""
WebSocket handlers for real-time communication.
"""

import json
from typing import Dict, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from loguru import logger

websocket_router = APIRouter()


class ConnectionManager:
    """Manages WebSocket connections."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.bot_connections: Dict[str, str] = {}  # bot_id -> connection_id
    
    async def connect(self, websocket: WebSocket, connection_id: str):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        logger.info(f"WebSocket connection established: {connection_id}")
    
    def disconnect(self, connection_id: str):
        """Remove a WebSocket connection."""
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
        
        # Remove bot connection mapping if exists
        for bot_id, conn_id in list(self.bot_connections.items()):
            if conn_id == connection_id:
                del self.bot_connections[bot_id]
                break
        
        logger.info(f"WebSocket connection closed: {connection_id}")
    
    async def send_personal_message(self, message: dict, connection_id: str):
        """Send a message to a specific connection."""
        if connection_id in self.active_connections:
            websocket = self.active_connections[connection_id]
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Failed to send message to {connection_id}: {e}")
                self.disconnect(connection_id)
    
    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients."""
        message_text = json.dumps(message)
        disconnected = []
        
        for connection_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(message_text)
            except Exception as e:
                logger.error(f"Failed to broadcast to {connection_id}: {e}")
                disconnected.append(connection_id)
        
        # Clean up disconnected connections
        for connection_id in disconnected:
            self.disconnect(connection_id)
    
    async def send_to_bot(self, message: dict, bot_id: str):
        """Send a message to a specific bot."""
        if bot_id in self.bot_connections:
            connection_id = self.bot_connections[bot_id]
            await self.send_personal_message(message, connection_id)
        else:
            logger.warning(f"Bot {bot_id} not connected via WebSocket")
    
    def register_bot(self, bot_id: str, connection_id: str):
        """Register a bot with a WebSocket connection."""
        self.bot_connections[bot_id] = connection_id
        logger.info(f"Bot {bot_id} registered with connection {connection_id}")


# Global connection manager
manager = ConnectionManager()


@websocket_router.websocket("/bot/{bot_id}")
async def bot_websocket_endpoint(websocket: WebSocket, bot_id: str):
    """WebSocket endpoint for bot connections."""
    connection_id = f"bot_{bot_id}"
    
    await manager.connect(websocket, connection_id)
    manager.register_bot(bot_id, connection_id)
    
    try:
        # Send welcome message
        await manager.send_personal_message({
            "type": "welcome",
            "bot_id": bot_id,
            "message": "Connected to Kentech Bot Pairing System"
        }, connection_id)
        
        while True:
            # Receive message from bot
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                await handle_bot_message(bot_id, message, connection_id)
            except json.JSONDecodeError:
                await manager.send_personal_message({
                    "type": "error",
                    "message": "Invalid JSON format"
                }, connection_id)
                
    except WebSocketDisconnect:
        manager.disconnect(connection_id)
        logger.info(f"Bot {bot_id} disconnected")


@websocket_router.websocket("/monitoring")
async def monitoring_websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for web interface monitoring."""
    connection_id = "web_monitor"
    
    await manager.connect(websocket, connection_id)
    
    try:
        # Send initial status
        await manager.send_personal_message({
            "type": "connected",
            "message": "Connected to monitoring feed",
            "active_connections": len(manager.active_connections),
            "connected_bots": len(manager.bot_connections)
        }, connection_id)
        
        while True:
            # Keep connection alive and handle any incoming messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "ping":
                await manager.send_personal_message({
                    "type": "pong",
                    "timestamp": message.get("timestamp")
                }, connection_id)
                
    except WebSocketDisconnect:
        manager.disconnect(connection_id)


@websocket_router.websocket("/monitor")
async def monitor_websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for monitoring connections."""
    connection_id = "monitor"
    
    await manager.connect(websocket, connection_id)
    
    try:
        # Send system status
        await manager.send_personal_message({
            "type": "status",
            "active_connections": len(manager.active_connections),
            "connected_bots": len(manager.bot_connections)
        }, connection_id)
        
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "ping":
                await manager.send_personal_message({
                    "type": "pong",
                    "timestamp": message.get("timestamp")
                }, connection_id)
                
    except WebSocketDisconnect:
        manager.disconnect(connection_id)


async def handle_bot_message(bot_id: str, message: dict, connection_id: str):
    """Handle incoming messages from bots."""
    message_type = message.get("type")
    
    if message_type == "heartbeat":
        # Handle heartbeat
        await manager.send_personal_message({
            "type": "heartbeat_ack",
            "timestamp": message.get("timestamp")
        }, connection_id)
        
    elif message_type == "status_update":
        # Handle status update
        status = message.get("status")
        logger.info(f"Bot {bot_id} status update: {status}")
        
        # Broadcast status update to monitors
        await manager.broadcast({
            "type": "bot_status_update",
            "bot_id": bot_id,
            "status": status,
            "timestamp": message.get("timestamp")
        })
        
    elif message_type == "pair_message":
        # Handle messages between paired bots
        target_bot_id = message.get("target_bot_id")
        if target_bot_id:
            await manager.send_to_bot({
                "type": "pair_message",
                "from_bot_id": bot_id,
                "message": message.get("message"),
                "timestamp": message.get("timestamp")
            }, target_bot_id)
        
    else:
        logger.warning(f"Unknown message type from bot {bot_id}: {message_type}")


async def notify_pair_created(pair_id: str, primary_bot_id: str, secondary_bot_id: str):
    """Notify about new pair creation."""
    notification = {
        "type": "pair_created",
        "pair_id": pair_id,
        "primary_bot_id": primary_bot_id,
        "secondary_bot_id": secondary_bot_id
    }
    
    # Notify the paired bots
    await manager.send_to_bot(notification, primary_bot_id)
    await manager.send_to_bot(notification, secondary_bot_id)
    
    # Broadcast to monitors
    await manager.broadcast(notification)


async def notify_pair_terminated(pair_id: str, primary_bot_id: str, secondary_bot_id: str):
    """Notify about pair termination."""
    notification = {
        "type": "pair_terminated",
        "pair_id": pair_id,
        "primary_bot_id": primary_bot_id,
        "secondary_bot_id": secondary_bot_id
    }
    
    # Notify the bots
    await manager.send_to_bot(notification, primary_bot_id)
    await manager.send_to_bot(notification, secondary_bot_id)
    
    # Broadcast to monitors
    await manager.broadcast(notification)
