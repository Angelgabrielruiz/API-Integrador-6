from app.infraestructure.websocket.manager import websocket_manager

from fastapi import FastAPI
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

# Importaciones de la Arquitectura
from app.core import db_postgresql as database
from app.infraestructure import routes
from app.domain.entities.maquina import Maquina
from app.domain.entities.producto import Producto
from app.domain.entities.contenedor import Contenedor
from app.domain.entities.sensor_reading import SensorReading
from app.domain.entities.usuario import Usuario

# Importar controlador de auth
from app.infraestructure.controllers import auth_controller

# Crea las tablas en la base de datos al iniciar (si no existen)
database.create_db_and_tables()

app = FastAPI(
    title="API Nutribox",
    version="1.0.0"
)

# --- Configuración de CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Inclusión de Rutas ---
app.include_router(routes.api_router, prefix="/api/v1")
app.include_router(auth_controller.router, prefix="/api/v1/auth", tags=["authentication"])  # Nueva ruta

@app.get("/")
def read_root():
    return {"status": "API Nutribox is running!"}

@app.websocket("/ws/sensores")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket_manager.broadcast(data)
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)