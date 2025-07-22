from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime
from app.application.useCase.venta_usecase import VentaUseCase
from app.infraestructure.schemas.venta_schema import VentaCreate, VentaSchema, VentaResponse
from app.dependencies import get_venta_use_case

router = APIRouter()

@router.post("/", response_model=VentaResponse, status_code=status.HTTP_201_CREATED)
def registrar_venta(
    venta_data: VentaCreate,
    use_case: VentaUseCase = Depends(get_venta_use_case)
):
    """Registra una nueva venta (usado internamente por el consumer)"""
    venta = use_case.registrar_venta(venta_data)
    return VentaResponse(
        message="Venta registrada exitosamente",
        venta=VentaSchema.from_orm(venta)
    )

@router.get("/", response_model=List[VentaSchema])
def get_todas_las_ventas(
    use_case: VentaUseCase = Depends(get_venta_use_case)
):
    """Obtiene todas las ventas"""
    return use_case.get_todas_las_ventas()

@router.get("/maquina/{maquina_id}", response_model=List[VentaSchema])
def get_ventas_por_maquina(
    maquina_id: int,
    use_case: VentaUseCase = Depends(get_venta_use_case)
):
    """Obtiene las ventas de una máquina específica"""
    return use_case.get_ventas_por_maquina(maquina_id)

@router.get("/maquina/{maquina_id}/total")
def get_total_ventas_maquina(
    maquina_id: int,
    use_case: VentaUseCase = Depends(get_venta_use_case)
):
    """Obtiene el total de ventas de una máquina"""
    total = use_case.get_total_ventas_maquina(maquina_id)
    return {"maquina_id": maquina_id, "total_ventas": total}

@router.get("/rango-fecha", response_model=List[VentaSchema])
def get_ventas_por_rango_fecha(
    fecha_inicio: datetime = Query(...),
    fecha_fin: datetime = Query(...),
    use_case: VentaUseCase = Depends(get_venta_use_case)
):
    """Obtiene ventas en un rango de fechas"""
    return use_case.get_ventas_por_rango_fecha(fecha_inicio, fecha_fin)