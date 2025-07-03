from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.db_postgresql import Base

class Contenedor(Base):
    __tablename__ = "contenedores"

    id_contenedor = Column(Integer, primary_key=True, index=True)
    id_maquina = Column(Integer, ForeignKey("maquinas.id_maquina"))
    id_producto = Column(Integer, ForeignKey("productos.id"))
    tipo = Column(String)
    capacidad_maxima = Column(Float)
    cantidad_actual = Column(Float)
    temperatura = Column(Float) 
    ultima_recarga = Column(DateTime(timezone=True), server_default=func.now())