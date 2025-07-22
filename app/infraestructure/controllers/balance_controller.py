from fastapi import APIRouter, Depends, HTTPException, status
from app.application.useCase.balance_usecase import BalanceUseCase
from app.infraestructure.schemas.balance_schema import BalanceSchema, AgregarCreditoRequest, ModificarBalanceRequest
from app.dependencies import get_balance_use_case

router = APIRouter()

@router.get("/maquina/{maquina_id}", response_model=BalanceSchema)
def get_balance_maquina(
    maquina_id: int,
    use_case: BalanceUseCase = Depends(get_balance_use_case)
):
    """Obtener el balance de una máquina"""
    balance = use_case.get_balance_maquina(maquina_id)
    if not balance:
        # Si no existe, crear uno con crédito 0
        balance = use_case.agregar_credito(maquina_id, 0.0)
    return balance

@router.post("/agregar-credito", response_model=BalanceSchema)
def agregar_credito(
    request: AgregarCreditoRequest,
    use_case: BalanceUseCase = Depends(get_balance_use_case)
):
    """Agregar crédito cuando se inserta una moneda"""
    balance = use_case.agregar_credito(request.maquina_id, request.cantidad)
    return balance

# NUEVO: Endpoint PUT para modificar balance directamente
@router.put("/maquina/{maquina_id}", response_model=BalanceSchema)
def modificar_balance(
    maquina_id: int,
    request: ModificarBalanceRequest,
    use_case: BalanceUseCase = Depends(get_balance_use_case)
):
    """Modificar el balance de una máquina directamente"""
    try:
        balance = use_case.modificar_balance(maquina_id, request.nuevo_credito)
        return balance
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/maquina/{maquina_id}/credito")
def get_credito_disponible(
    maquina_id: int,
    use_case: BalanceUseCase = Depends(get_balance_use_case)
):
    """Obtener solo el crédito disponible"""
    credito = use_case.get_credito_disponible(maquina_id)
    return {"maquina_id": maquina_id, "credito_disponible": credito}