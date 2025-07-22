from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from app.core.db_postgresql import Base

class Venta(Base):
    __tablename__ = "ventas"

    id_venta = Column(Integer, primary_key=True, index=True)
    id_maquina = Column(Integer, ForeignKey("maquinas.id_maquina"))
    id_producto = Column(Integer, ForeignKey("productos.id"))
    cantidad_dispensada = Column(Float)
    precio_unitario = Column(Float)
    total_venta = Column(Float)
    pin_valvula = Column(Integer, nullable=True)  # Para identificar qué válvula se usó
    estado = Column(String, default="completado")  # completado, fallido, etc.
    fecha_venta = Column(DateTime(timezone=True), server_default=func.now())
    metodo_dispensado = Column(String)  # "valvula" o "venta_directa"