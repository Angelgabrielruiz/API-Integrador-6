from pydantic import BaseModel
from typing import Optional

# Propiedades base compartidas
class ProductoBase(BaseModel):
    nombre: str
    precio: float
    descripcion: Optional[str] = None

# Propiedades para recibir en la creación
class ProductoCreate(ProductoBase):
    pass

# Propiedades para recibir en la actualización (todos los campos son opcionales)
class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    descripcion: Optional[str] = None

# Propiedades para devolver al cliente (incluye el ID)
class ProductoSchema(ProductoBase):
    id: int

    class Config:
        from_attributes = True # Permite a Pydantic leer datos desde objetos ORM