from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.application.useCase.producto_usecase import ProductoUseCase
from app.infraestructure.schemas.producto_schema import ProductoCreate, ProductoSchema, ProductoUpdate
from app.dependencies import get_producto_use_case
from app.infraestructure.middleware.auth_middleware import require_admin, require_client_or_admin
from app.domain.entities.usuario import Usuario

router = APIRouter()

# Solo administradores pueden crear productos
@router.post("/", response_model=ProductoSchema, status_code=status.HTTP_201_CREATED)
def create_producto(
    producto: ProductoCreate, 
    use_case: ProductoUseCase = Depends(get_producto_use_case),
    current_user: Usuario = Depends(require_admin)  # Solo admin
):
    return use_case.create_producto(producto_data=producto)

# Clientes y administradores pueden ver productos (DESPROTEGIDO)
@router.get("/", response_model=List[ProductoSchema])
def get_all_productos(
    use_case: ProductoUseCase = Depends(get_producto_use_case)
    # Remover: current_user: Usuario = Depends(require_client_or_admin)
):
    return use_case.get_all_productos()

@router.get("/{producto_id}", response_model=ProductoSchema)
def get_producto(
    producto_id: int, 
    use_case: ProductoUseCase = Depends(get_producto_use_case)
    # Mantener sin protección
):
    producto = use_case.get_producto_by_id(producto_id)
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return producto

@router.put("/{producto_id}", response_model=ProductoSchema)
def update_producto(
    producto_id: int, 
    producto_data: ProductoUpdate, 
    use_case: ProductoUseCase = Depends(get_producto_use_case),
    current_user: Usuario = Depends(require_admin)  # Agregar protección admin
):
    updated_producto = use_case.update_producto(producto_id, producto_data)
    if not updated_producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return updated_producto

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(
    producto_id: int, 
    use_case: ProductoUseCase = Depends(get_producto_use_case),
    current_user: Usuario = Depends(require_admin)  # Agregar protección admin
):
    deleted = use_case.delete_producto(producto_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return