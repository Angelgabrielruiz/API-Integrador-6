import uuid
from sqlalchemy import Column, String, Numeric, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.core.db_postgresql import Base

class SensorReading(Base):
    __tablename__ = 'sensor_readings'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    machine_id = Column(String, nullable=False)
    sensor_type = Column(String, nullable=False)
    value_numeric = Column(Numeric, nullable=False)
    unit = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())