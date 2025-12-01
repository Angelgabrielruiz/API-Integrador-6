from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VentaCreate(BaseModel):
    id_maquina: int
    id_producto: int
    cantidad_dispensada: float
    precio_unitario: Optional[float] = None  # ← HACER OPCIONAL
    pin_valvula: Optional[int] = None
    metodo_dispensado: str = "valvula"

class VentaSchema(BaseModel):
    id_venta: int
    id_maquina: int
    id_producto: int
    cantidad_dispensada: float
    precio_unitario: float
    total_venta: float
    pin_valvula: Optional[int]
    estado: str
    fecha_venta: datetime
    metodo_dispensado: str

    class Config:
        from_attributes = True

class VentaResponse(BaseModel):
    message: str
    venta: VentaSchema