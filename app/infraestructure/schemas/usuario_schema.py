from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    username: str
    email: EmailStr
    role: str = "administrador"  # Cambiado de "cliente" a "administrador"

class UsuarioCreate(UsuarioBase):
    password: str = Field(min_length=4)

class UsuarioLogin(BaseModel):
    username: str
    password: str

class UsuarioSchema(UsuarioBase):
    id: int  # Cambiado de uuid.UUID a int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UsuarioSchema

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None
