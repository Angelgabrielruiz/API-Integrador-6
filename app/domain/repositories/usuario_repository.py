from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.usuario import Usuario

class IUsuarioRepository(ABC):
    
    @abstractmethod
    def find_by_username(self, username: str) -> Optional[Usuario]:
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Usuario]:
        pass
    
    @abstractmethod
    def save(self, usuario: Usuario) -> Usuario:
        pass