from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.application.useCase.contenedor_usecase import ContenedorUseCase
from app.infraestructure.schemas.contenedor_schema import ContenedorCreate, ContenedorSchema, ContenedorUpdate, DispensarRequest
from app.dependencies import get_contenedor_use_case # This will be created in the next step

router = APIRouter()

@router.post("/dispensar", response_model=ContenedorSchema)
def dispensar_producto(
    dispensar_request: DispensarRequest,
    use_case: ContenedorUseCase = Depends(get_contenedor_use_case)
):
    try:
        updated_contenedor = use_case.dispensar_producto(dispensar_request)
        if not updated_contenedor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contenedor no encontrado para esa máquina y producto.")
        return updated_contenedor
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/", response_model=ContenedorSchema, status_code=status.HTTP_201_CREATED)
def create_contenedor(
    contenedor: ContenedorCreate, 
    use_case: ContenedorUseCase = Depends(get_contenedor_use_case)
):
    return use_case.create_contenedor(contenedor_data=contenedor)

@router.get("/", response_model=List[ContenedorSchema])
def get_all_contenedores(use_case: ContenedorUseCase = Depends(get_contenedor_use_case)):
    return use_case.get_all_contenedores()

@router.get("/{contenedor_id}", response_model=ContenedorSchema)
def get_contenedor(
    contenedor_id: int, 
    use_case: ContenedorUseCase = Depends(get_contenedor_use_case)
):
    contenedor = use_case.get_contenedor_by_id(contenedor_id)
    if not contenedor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contenedor no encontrado")
    return contenedor

@router.put("/{contenedor_id}", response_model=ContenedorSchema)
def update_contenedor(
    contenedor_id: int, 
    contenedor_data: ContenedorUpdate, 
    use_case: ContenedorUseCase = Depends(get_contenedor_use_case)
):
    updated_contenedor = use_case.update_contenedor(contenedor_id, contenedor_data)
    if not updated_contenedor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contenedor no encontrado")
    return updated_contenedor

@router.delete("/{contenedor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contenedor(
    contenedor_id: int, 
    use_case: ContenedorUseCase = Depends(get_contenedor_use_case)
):
    deleted = use_case.delete_contenedor(contenedor_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contenedor no encontrado")
    return

@router.put("/{contenedor_id}/temperatura", response_model=ContenedorSchema)
def actualizar_temperatura(
    contenedor_id: int,
    temperatura_data: dict,  # Cambiar para recibir JSON body
    use_case: ContenedorUseCase = Depends(get_contenedor_use_case)
):
    contenedor = use_case.get_contenedor_by_id(contenedor_id)
    if not contenedor:
        raise HTTPException(status_code=404, detail="Contenedor no encontrado")
    
    # Usar ContenedorUpdate para la actualización
    update_data = ContenedorUpdate(temperatura=temperatura_data.get('temperatura'))
    return use_case.update_contenedor(contenedor_id, update_data)