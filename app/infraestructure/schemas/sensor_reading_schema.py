from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class SensorReadingBase(BaseModel):
    machine_id: str
    sensor_type: str
    value_numeric: float
    unit: Optional[str] = None

class SensorReadingCreate(SensorReadingBase):
    pass

class SensorReadingSchema(SensorReadingBase):
    id: uuid.UUID
    timestamp: datetime

    class Config:
        from_attributes = True