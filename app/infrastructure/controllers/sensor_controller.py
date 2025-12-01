from fastapi import APIRouter, Depends, status
from typing import List
from app.application.useCase.sensor_usecase import SensorUseCase
from app.infrastructure.schemas.sensor_reading_schema import SensorReadingCreate, SensorReadingSchema
from app.dependencies import get_sensor_use_case
from app.infrastructure.websocket.manager import websocket_manager
from app.infrastructure.middleware.auth_middleware import require_admin
from app.domain.entities.usuario import Usuario
from decimal import Decimal

router = APIRouter()

# POST desprotegido - cualquiera puede crear lecturas de sensores
@router.post("/", response_model=SensorReadingSchema, status_code=status.HTTP_201_CREATED)
async def create_sensor_reading(
    sensor_reading: SensorReadingCreate, 
    use_case: SensorUseCase = Depends(get_sensor_use_case)
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
    current_user: Usuario = Depends(require_admin)
):
    return use_case.get_all_sensor_readings()

# NUEVO: DELETE específico para sensores de moneda
@router.delete("/moneda", status_code=status.HTTP_200_OK)
def delete_coin_sensors(
    use_case: SensorUseCase = Depends(get_sensor_use_case),
    current_user: Usuario = Depends(require_admin)
):
    """Elimina todos los registros de sensores de tipo 'moneda'"""
    deleted_count = use_case.delete_coin_sensors()
    return {
        "message": f"Se eliminaron {deleted_count} registros de sensores de moneda",
        "deleted_count": deleted_count
    }

# NUEVO: DELETE genérico por tipo de sensor
@router.delete("/tipo/{sensor_type}", status_code=status.HTTP_200_OK)
def delete_sensors_by_type(
    sensor_type: str,
    use_case: SensorUseCase = Depends(get_sensor_use_case),
    current_user: Usuario = Depends(require_admin)
):
    """Elimina todos los registros de sensores del tipo especificado"""
    deleted_count = use_case.delete_sensors_by_type(sensor_type)
    return {
        "message": f"Se eliminaron {deleted_count} registros de sensores de tipo '{sensor_type}'",
        "deleted_count": deleted_count,
        "sensor_type": sensor_type
    }