from sqlalchemy import Column, Integer, Float, DateTime, func
from app.core.db_postgresql import Base

class Balance(Base):
    __tablename__ = "balances"

    id = Column(Integer, primary_key=True, index=True)
    id_maquina = Column(Integer, nullable=False, unique=True)  # Una máquina = un balance
    credito_actual = Column(Float, default=0.0)  # Dinero disponible
    fecha_actualizacion = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())