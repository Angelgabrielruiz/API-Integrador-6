from fastapi.websockets import WebSocket
from typing import List, Dict, Any, Union
import json
from datetime import datetime
from decimal import Decimal
import logging

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.logger = logging.getLogger(__name__)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.logger.info(
            "websocket_connected",
            extra={"connection_count": len(self.active_connections)}
        )

    async def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            try:
                await websocket.close()
            except Exception:
                pass
            self.active_connections.remove(websocket)
            self.logger.info(
                "websocket_disconnected",
                extra={"connection_count": len(self.active_connections)}
            )

    def _serialize_data(self, data: Any) -> Any:
        """Convierte tipos no serializables a tipos compatibles con JSON"""
        if isinstance(data, Decimal):
            return float(data)
        elif isinstance(data, datetime):
            return data.isoformat()
        elif isinstance(data, dict):
            return {key: self._serialize_data(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._serialize_data(item) for item in data]
        else:
            return data

    async def send_personal_message(self, message: Union[str, Dict[str, Any]], websocket: WebSocket):
        try:
            if isinstance(message, str):
                await websocket.send_text(message)
            else:
                # Serializar datos antes de enviar
                serialized_message = self._serialize_data(message)
                await websocket.send_json(serialized_message)
        except Exception as e:
            self.logger.error(
                "websocket_personal_message_error",
                extra={"error": str(e)}
            )
            await self.disconnect(websocket)

    async def broadcast(self, message: Union[str, Dict[str, Any]]):
        if not self.active_connections:
            return
        
        # Si es string, intentar convertir a JSON
        if isinstance(message, str):
            try:
                message = json.loads(message)
            except json.JSONDecodeError:
                message = {"type": "message", "content": message}
        
        # Agregar timestamp si no existe
        if isinstance(message, dict) and "timestamp" not in message:
            message["timestamp"] = datetime.now().isoformat()
        
        # Serializar datos
        serialized_message = self._serialize_data(message)
        
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(serialized_message)
            except Exception as e:
                self.logger.error(
                    "websocket_broadcast_error",
                    extra={"error": str(e)}
                )
                disconnected.append(connection)
        
        # Remover conexiones desconectadas
        for conn in disconnected:
            await self.disconnect(conn)

    def get_connection_count(self) -> int:
        return len(self.active_connections)
