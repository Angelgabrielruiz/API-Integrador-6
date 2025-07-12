from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from app.core.database_deps import get_db_session  # Cambiar esta línea
from app.infraestructure.adapters.usuario_postgres_repository import UsuarioPostgresRepository
from app.infraestructure.schemas.usuario_schema import TokenData
from app.domain.entities.usuario import Usuario

# Configuración JWT
SECRET_KEY = "tu_clave_secreta_muy_segura_aqui_cambiala_en_produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token_data: TokenData = Depends(verify_token), db: Session = Depends(get_db_session)):
    usuario_repo = UsuarioPostgresRepository(db)
    user = usuario_repo.find_by_username(username=token_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

def require_admin(current_user: Usuario = Depends(get_current_user)):
    if current_user.role != "administrador":  # Cambiado de "admin" a "administrador"
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

def require_client_or_admin(current_user: Usuario = Depends(get_current_user)):
    if current_user.role not in ["cliente", "administrador"]:  # Actualizado roles
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Client or Admin access required"
        )
    return current_user