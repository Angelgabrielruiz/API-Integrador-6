from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from typing import List, Optional
import uuid
from app.application.useCase.producto_usecase import ProductoUseCase
from app.infrastructure.schemas.producto_schema import ProductoCreate, ProductoSchema, ProductoUpdate
from app.dependencies import get_producto_use_case
from app.infrastructure.middleware.auth_middleware import require_admin, require_client_or_admin
from app.domain.entities.usuario import Usuario
from app.infrastructure.services.cloudinary_service import CloudinaryService

router = APIRouter()
cloudinary_service = CloudinaryService()

# Solo administradores pueden crear productos
@router.post("/", response_model=ProductoSchema, status_code=status.HTTP_201_CREATED)
async def create_producto(
    nombre: str = Form(...),
    precio: float = Form(...),
    descripcion: Optional[str] = Form(None),
    imagen: Optional[UploadFile] = File(None),
    use_case: ProductoUseCase = Depends(get_producto_use_case),
    current_user: Usuario = Depends(require_admin)
):
    public_id = None
    
    try:
        # Validaciones básicas
        if not nombre or nombre.strip() == "":
            raise HTTPException(status_code=400, detail="El nombre es requerido")
        
        if precio <= 0:
            raise HTTPException(status_code=400, detail="El precio debe ser mayor a 0")
        
        # Procesar imagen si se proporciona
        url_imagen = None
        public_id_imagen = None
        
        if imagen:
            # Validar tipo de archivo
            if not imagen.content_type or not imagen.content_type.startswith("image/"):
                raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
            
            # Validar tamaño (máximo 5MB)
            if imagen.size > 5 * 1024 * 1024:
                raise HTTPException(status_code=400, detail="El archivo es demasiado grande (máximo 5MB)")
            
            # Generar ID único para la imagen
            public_id = f"producto_{uuid.uuid4()}"
            
            # Leer y subir imagen
            image_bytes = await imagen.read()
            url_imagen = cloudinary_service.upload_image(image_bytes, public_id)
            public_id_imagen = public_id
        
        # Crear objeto producto
        producto_data = ProductoCreate(
            nombre=nombre.strip(),
            precio=precio,
            descripcion=descripcion.strip() if descripcion else None
        )
        
        # Crear producto con imagen
        producto = use_case.create_producto_with_image(
            producto_data=producto_data,
            url_imagen=url_imagen,
            public_id_imagen=public_id_imagen
        )
        
        return producto
        
    except HTTPException:
        # Si hay error y se subió imagen, eliminarla
        if public_id:
            cloudinary_service.delete_image(public_id)
        raise
    except Exception as e:
        # Si hay error y se subió imagen, eliminarla
        if public_id:
            cloudinary_service.delete_image(public_id)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

# Clientes y administradores pueden ver productos (DESPROTEGIDO)
@router.get("/", response_model=List[ProductoSchema])
def get_all_productos(
    use_case: ProductoUseCase = Depends(get_producto_use_case)
):
    return use_case.get_all_productos()

@router.get("/{producto_id}", response_model=ProductoSchema)
def get_producto(
    producto_id: int, 
    use_case: ProductoUseCase = Depends(get_producto_use_case)
):
    producto = use_case.get_producto_by_id(producto_id)
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return producto

@router.put("/{producto_id}", response_model=ProductoSchema)
async def update_producto(
    producto_id: int,
    nombre: Optional[str] = Form(None),
    precio: Optional[float] = Form(None),
    descripcion: Optional[str] = Form(None),
    imagen: Optional[UploadFile] = File(None),
    use_case: ProductoUseCase = Depends(get_producto_use_case),
    current_user: Usuario = Depends(require_admin)
):
    public_id = None
    
    try:
        # Validaciones
        if precio is not None and precio <= 0:
            raise HTTPException(status_code=400, detail="El precio debe ser mayor a 0")
        
        # Procesar imagen si se proporciona
        url_imagen = None
        public_id_imagen = None
        
        if imagen:
            # Validar tipo de archivo
            if not imagen.content_type or not imagen.content_type.startswith("image/"):
                raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
            
            # Validar tamaño (máximo 5MB)
            if imagen.size > 5 * 1024 * 1024:
                raise HTTPException(status_code=400, detail="El archivo es demasiado grande (máximo 5MB)")
            
            # Generar ID único para la imagen
            public_id = f"producto_{uuid.uuid4()}"
            
            # Leer y subir imagen
            image_bytes = await imagen.read()
            url_imagen = cloudinary_service.upload_image(image_bytes, public_id)
            public_id_imagen = public_id
        
        # Crear objeto de actualización
        update_data = {}
        if nombre is not None:
            update_data["nombre"] = nombre.strip()
        if precio is not None:
            update_data["precio"] = precio
        if descripcion is not None:
            update_data["descripcion"] = descripcion.strip()
        
        producto_data = ProductoUpdate(**update_data)
        
        # Actualizar producto
        updated_producto = use_case.update_producto_with_image(
            producto_id=producto_id,
            producto_data=producto_data,
            url_imagen=url_imagen,
            public_id_imagen=public_id_imagen
        )
        
        if not updated_producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        
        return updated_producto
        
    except HTTPException:
        # Si hay error y se subió imagen, eliminarla
        if public_id:
            cloudinary_service.delete_image(public_id)
        raise
    except Exception as e:
        # Si hay error y se subió imagen, eliminarla
        if public_id:
            cloudinary_service.delete_image(public_id)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(
    producto_id: int, 
    use_case: ProductoUseCase = Depends(get_producto_use_case),
    current_user: Usuario = Depends(require_admin)
):
    deleted = use_case.delete_producto(producto_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return