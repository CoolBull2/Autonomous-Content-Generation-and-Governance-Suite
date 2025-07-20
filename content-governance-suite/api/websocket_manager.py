from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
import asyncio

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str = None):
        await websocket.accept()
        self.active_connections.append(websocket)
        if user_id:
            self.user_connections[user_id] = websocket
    
    def disconnect(self, websocket: WebSocket, user_id: str = None):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if user_id and user_id in self.user_connections:
            del self.user_connections[user_id]
    
    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.user_connections:
            await self.user_connections[user_id].send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass
    
    async def send_generation_update(self, step: str, progress: int, user_id: str = None):
        message = {
            "type": "generation_update",
            "step": step,
            "progress": progress,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        if user_id:
            await self.send_personal_message(json.dumps(message), user_id)
        else:
            await self.broadcast(json.dumps(message))

# Global WebSocket manager instance
ws_manager = WebSocketManager()
