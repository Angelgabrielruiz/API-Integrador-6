from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ContenedorBase(BaseModel):
    id_maquina: int
    id_producto: int
    tipo: str
    capacidad_maxima: float
    cantidad_actual: float
    temperatura: Optional[float] = None  # Hacer opcional

class ContenedorCreate(ContenedorBase):
    pass

class ContenedorUpdate(BaseModel):
    id_maquina: Optional[int] = None
    id_producto: Optional[int] = None
    tipo: Optional[str] = None
    capacidad_maxima: Optional[float] = None
    cantidad_actual: Optional[float] = None
    temperatura: Optional[float] = None
class TemperaturaUpdate(BaseModel):
    temperatura: float

class DispensarRequest(BaseModel):
    id_maquina: int
    id_producto: int
    cantidad_dispensada: float


class ContenedorSchema(ContenedorBase):
    id_contenedor: int
    ultima_recarga: datetime

    class Config:
        from_attributes = True