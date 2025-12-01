from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BalanceBase(BaseModel):
    id_maquina: int
    credito_actual: float

class BalanceCreate(BalanceBase):
    pass

class BalanceSchema(BalanceBase):
    id: int
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True

class AgregarCreditoRequest(BaseModel):
    maquina_id: int
    cantidad: float

# NUEVO: Esquema para modificar balance directamente
class ModificarBalanceRequest(BaseModel):
    nuevo_credito: float