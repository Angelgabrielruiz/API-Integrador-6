from sqlalchemy import Column, Integer, Boolean
from app.core.db_postgresql import Base

class Maquina(Base):
    __tablename__ = "maquinas"

    id_maquina = Column(Integer, primary_key=True, index=True)
    estado = Column(Boolean, default=True)