from typing import List
from datetime import datetime
from app.domain.repositories.venta_repository import IVentaRepository
from app.domain.repositories.product_repository import IProductoRepository
from app.domain.entities.venta import Venta
from app.infrastructure.schemas.venta_schema import VentaCreate
from fastapi import HTTPException

class VentaUseCase:
    def __init__(self, venta_repository: IVentaRepository, producto_repository: IProductoRepository):
        self.venta_repository = venta_repository
        self.producto_repository = producto_repository

    def registrar_venta(self, venta_data: VentaCreate) -> Venta:
        # Obtener el precio del producto
        producto = self.producto_repository.find_by_id(venta_data.id_producto)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        # Usar el precio del esquema si se proporciona, sino usar el del producto
        precio_unitario = venta_data.precio_unitario or producto.precio
        
        # CAMBIO: El total de venta es el precio fijo del producto (no multiplicado por cantidad)
        total_venta = precio_unitario  # ← Solo el precio del producto
        
        # Crear la venta
        venta = Venta(
            id_maquina=venta_data.id_maquina,
            id_producto=venta_data.id_producto,
            cantidad_dispensada=venta_data.cantidad_dispensada,
            precio_unitario=precio_unitario,
            total_venta=total_venta,  # ← Ahora será siempre $5
            pin_valvula=venta_data.pin_valvula,
            metodo_dispensado=venta_data.metodo_dispensado
        )
        
        return self.venta_repository.save(venta)

    def get_ventas_por_maquina(self, maquina_id: int) -> List[Venta]:
        return self.venta_repository.find_by_maquina(maquina_id)

    def get_todas_las_ventas(self) -> List[Venta]:
        return self.venta_repository.find_all()

    def get_ventas_por_rango_fecha(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[Venta]:
        return self.venta_repository.find_by_fecha_rango(fecha_inicio, fecha_fin)

    def get_total_ventas_maquina(self, maquina_id: int) -> float:
        return self.venta_repository.get_total_ventas_por_maquina(maquina_id)