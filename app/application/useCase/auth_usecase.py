from typing import Optional
from fastapi import HTTPException, status
from app.domain.repositories.usuario_repository import IUsuarioRepository
from app.domain.entities.usuario import Usuario
from app.infraestructure.schemas.usuario_schema import UsuarioCreate, UsuarioLogin, Token
from app.infraestructure.middleware.auth_middleware import create_access_token
from datetime import timedelta

class AuthUseCase:
    
    def __init__(self, usuario_repository: IUsuarioRepository):
        self.usuario_repository = usuario_repository
    
    def register_user(self, user_data: UsuarioCreate) -> Usuario:
        # Verificar si el usuario ya existe
        existing_user = self.usuario_repository.find_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        existing_email = self.usuario_repository.find_by_email(user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Crear nuevo usuario
        usuario = Usuario(
            username=user_data.username,
            email=user_data.email,
            password=Usuario.hash_password(user_data.password),  # Hashear directamente
            role=user_data.role
        )
        
        return self.usuario_repository.save(usuario)
    
    def authenticate_user(self, login_data: UsuarioLogin) -> Token:
        user = self.usuario_repository.find_by_username(login_data.username)
        if not user or not user.verify_password(login_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.username, "role": user.role},
            expires_delta=access_token_expires
        )
        
        from app.infraestructure.schemas.usuario_schema import UsuarioSchema
        user_schema = UsuarioSchema.from_orm(user)
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user_schema
        )