from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities.sensor_reading import SensorReading
from app.domain.repositories.sensor_reading_repository import ISensorReadingRepository
import uuid

class SensorReadingPostgresRepository(ISensorReadingRepository):

    def __init__(self, db_session: Session):
        self.db = db_session

    def find_by_id(self, sensor_reading_id: uuid.UUID) -> Optional[SensorReading]:
        return self.db.query(SensorReading).filter(SensorReading.id == sensor_reading_id).first()

    def find_all(self) -> List[SensorReading]:
        return self.db.query(SensorReading).all()

    def save(self, sensor_reading_data: SensorReading) -> SensorReading:
        self.db.add(sensor_reading_data)
        self.db.commit()
        self.db.refresh(sensor_reading_data)
        return sensor_reading_data