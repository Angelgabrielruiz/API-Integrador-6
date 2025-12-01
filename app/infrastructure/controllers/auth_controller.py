from fastapi import APIRouter, Depends, HTTPException, status
from app.application.useCase.auth_usecase import AuthUseCase
from app.infrastructure.schemas.usuario_schema import UsuarioCreate, UsuarioLogin, Token, UsuarioSchema
from app.dependencies import get_auth_use_case
from app.infrastructure.middleware.auth_middleware import get_current_user, require_admin  # Agregar require_admin
from app.domain.entities.usuario import Usuario

router = APIRouter()

@router.post("/register", response_model=UsuarioSchema, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UsuarioCreate,
    use_case: AuthUseCase = Depends(get_auth_use_case)
):
    return use_case.register_user(user_data)

@router.post("/login", response_model=Token)
def login(
    login_data: UsuarioLogin,
    use_case: AuthUseCase = Depends(get_auth_use_case)
):
    return use_case.authenticate_user(login_data)

@router.get("/me", response_model=UsuarioSchema)
def get_current_user_info(current_user: Usuario = Depends(get_current_user)):
    return current_user

@router.get("/admin-only")
def admin_only_endpoint(current_user: Usuario = Depends(require_admin)):
    return {"message": "Hello Admin!", "user": current_user.username}