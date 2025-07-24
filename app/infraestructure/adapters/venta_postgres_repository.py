from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.domain.repositories.venta_repository import IVentaRepository
from app.domain.entities.venta import Venta

class VentaPostgresRepository(IVentaRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_all(self) -> List[Venta]:
        return self.session.query(Venta).all()

    def find_by_id(self, venta_id: int) -> Optional[Venta]:
        return self.session.query(Venta).filter(Venta.id_venta == venta_id).first()

    def find_by_maquina(self, maquina_id: int) -> List[Venta]:
        return self.session.query(Venta).filter(Venta.id_maquina == maquina_id).all()

    def find_by_fecha_rango(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[Venta]:
        return self.session.query(Venta).filter(
            Venta.fecha_venta >= fecha_inicio,
            Venta.fecha_venta <= fecha_fin
        ).all()

    def save(self, venta: Venta) -> Venta:
        self.session.add(venta)
        self.session.commit()
        self.session.refresh(venta)
        return venta

    def get_ventas_por_producto(self, producto_id: int) -> List[Venta]:
        return self.session.query(Venta).filter(Venta.id_producto == producto_id).all()

    def get_total_ventas_por_maquina(self, maquina_id: int) -> float:
        result = self.session.query(func.sum(Venta.total_venta)).filter(
            Venta.id_maquina == maquina_id
        ).scalar()
        return result or 0.0
    
    # NUEVO: Implementación para eliminar ventas por producto
    def delete_ventas_por_producto(self, producto_id: int) -> int:
        ventas_eliminadas = self.session.query(Venta).filter(Venta.id_producto == producto_id).delete()
        self.session.commit()
        return ventas_eliminadas