from fastapi import APIRouter, Depends, status
from typing import List
from app.application.useCase.sensor_usecase import SensorUseCase
from app.infraestructure.schemas.sensor_reading_schema import SensorReadingCreate, SensorReadingSchema
from app.dependencies import get_sensor_use_case
from app.infraestructure.websocket.manager import websocket_manager
from app.infraestructure.middleware.auth_middleware import require_admin  # Mantener para GET
from app.domain.entities.usuario import Usuario  # Mantener para GET
from decimal import Decimal

router = APIRouter()

# POST desprotegido - cualquiera puede crear lecturas de sensores
@router.post("/", response_model=SensorReadingSchema, status_code=status.HTTP_201_CREATED)
async def create_sensor_reading(
    sensor_reading: SensorReadingCreate, 
    use_case: SensorUseCase = Depends(get_sensor_use_case)
    # Remover: current_user: Usuario = Depends(require_admin)
):
    # Crear la lectura del sensor
    result = use_case.create_sensor_reading(sensor_reading_data=sensor_reading)
    
    # Convertir Decimal a float para serialización JSON
    value_numeric = float(result.value_numeric) if isinstance(result.value_numeric, Decimal) else result.value_numeric
    
    # Enviar datos en tiempo real via WebSocket
    sensor_data = {
        "type": "sensor_data",
        "data": {
            "machine_id": result.machine_id,
            "sensor_type": result.sensor_type,
            "value_numeric": value_numeric,
            "unit": result.unit,
            "timestamp": result.timestamp.isoformat() if hasattr(result, 'timestamp') and result.timestamp else None
        }
    }
    
    await websocket_manager.broadcast(sensor_data)
    
    return result

# GET protegido - solo administradores pueden consultar lecturas
@router.get("/", response_model=List[SensorReadingSchema])
def get_all_sensor_readings(
    use_case: SensorUseCase = Depends(get_sensor_use_case),
    current_user: Usuario = Depends(require_admin)  # Mantener protección admin
):
    return use_case.get_all_sensor_readings()