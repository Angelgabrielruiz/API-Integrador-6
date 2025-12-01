from pydantic import BaseModel
from typing import Optional

class MaquinaBase(BaseModel):
    estado: bool

class MaquinaCreate(MaquinaBase):
    pass

class MaquinaUpdate(BaseModel):
    estado: Optional[bool] = None

class MaquinaSchema(MaquinaBase):
    id_maquina: int

    class Config:
        from_attributes = True