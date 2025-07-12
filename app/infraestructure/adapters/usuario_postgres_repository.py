from typing import Optional
from sqlalchemy.orm import Session
from app.domain.entities.usuario import Usuario
from app.domain.repositories.usuario_repository import IUsuarioRepository

class UsuarioPostgresRepository(IUsuarioRepository):
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def find_by_username(self, username: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.username == username).first()
    
    def find_by_email(self, email: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.email == email).first()
    
    def save(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario