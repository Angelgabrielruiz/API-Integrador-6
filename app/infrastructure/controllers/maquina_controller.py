from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.application.useCase.maquina_usecase import MaquinaUseCase
from app.infrastructure.schemas.maquina_schema import MaquinaCreate, MaquinaSchema, MaquinaUpdate
from app.dependencies import get_maquina_use_case

router = APIRouter()

@router.post("/", response_model=MaquinaSchema, status_code=status.HTTP_201_CREATED)
def create_maquina(
    maquina: MaquinaCreate, 
    use_case: MaquinaUseCase = Depends(get_maquina_use_case)
):
    return use_case.create_maquina(maquina_data=maquina)

@router.get("/", response_model=List[MaquinaSchema])
def get_all_maquinas(use_case: MaquinaUseCase = Depends(get_maquina_use_case)):
    return use_case.get_all_maquinas()

@router.get("/{maquina_id}", response_model=MaquinaSchema)
def get_maquina(
    maquina_id: int, 
    use_case: MaquinaUseCase = Depends(get_maquina_use_case)
):
    maquina = use_case.get_maquina_by_id(maquina_id)
    if not maquina:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Máquina no encontrada")
    return maquina

@router.put("/{maquina_id}", response_model=MaquinaSchema)
def update_maquina(
    maquina_id: int, 
    maquina_data: MaquinaUpdate, 
    use_case: MaquinaUseCase = Depends(get_maquina_use_case)
):
    updated_maquina = use_case.update_maquina(maquina_id, maquina_data)
    if not updated_maquina:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Máquina no encontrada")
    return updated_maquina

@router.delete("/{maquina_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_maquina(
    maquina_id: int, 
    use_case: MaquinaUseCase = Depends(get_maquina_use_case)
):
    deleted = use_case.delete_maquina(maquina_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Máquina no encontrada")
    return