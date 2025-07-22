from pydantic import BaseModel
from typing import Optional

class ValvulaRequest(BaseModel):
    id_maquina: int
    id_producto: int
    pin_valvula: int  # Pin específico de la válvula
    cantidad_solicitada: float  # Cantidad que se va a dispensar
    accion: str  # "abrir" o "cerrar"

class ValvulaResponse(BaseModel):
    id_maquina: int
    id_producto: int
    pin_valvula: int
    cantidad_dispensada: float
    estado: str  # "completado", "error", etc.