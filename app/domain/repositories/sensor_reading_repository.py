from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.sensor_reading import SensorReading
import uuid

class ISensorReadingRepository(ABC):

    @abstractmethod
    def find_by_id(self, sensor_reading_id: uuid.UUID) -> Optional[SensorReading]:
        pass

    @abstractmethod
    def find_all(self) -> List[SensorReading]:
        pass

    @abstractmethod
    def save(self, sensor_reading_data: SensorReading) -> SensorReading:
        pass
    
    # NUEVO: Método para eliminar sensores por tipo
    @abstractmethod
    def delete_by_sensor_type(self, sensor_type: str) -> int:
        pass