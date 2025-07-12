import uuid
from sqlalchemy import Column, String, Boolean, DateTime, func, Integer
from app.core.db_postgresql import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)  # Cambiado de UUID a Integer
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  # Cambiado de hashed_password a password
    role = Column(String(20), nullable=False, default="administrador")  # Cambiado default
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)  # Cambiado campo
    
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    def set_password(self, plain_password: str):
        """Establece una nueva contraseña hasheada"""
        self.password = self.hash_password(plain_password)