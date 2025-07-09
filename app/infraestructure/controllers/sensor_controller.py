from fastapi import APIRouter, Depends, status
from typing import List
from app.application.useCase.sensor_usecase import SensorUseCase
from app.infraestructure.schemas.sensor_reading_schema import SensorReadingCreate, SensorReadingSchema
from app.dependencies import get_sensor_use_case # We will create this dependency next

router = APIRouter()

@router.post("/", response_model=SensorReadingSchema, status_code=status.HTTP_201_CREATED)
def create_sensor_reading(
    sensor_reading: SensorReadingCreate, 
    use_case: SensorUseCase = Depends(get_sensor_use_case)
):
    return use_case.create_sensor_reading(sensor_reading_data=sensor_reading)

@router.get("/", response_model=List[SensorReadingSchema])
def get_all_sensor_readings(use_case: SensorUseCase = Depends(get_sensor_use_case)):
    return use_case.get_all_sensor_readings()