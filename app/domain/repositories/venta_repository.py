from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from app.domain.entities.venta import Venta

class IVentaRepository(ABC):
    
    @abstractmethod
    def find_all(self) -> List[Venta]:
        pass

    @abstractmethod
    def find_by_id(self, venta_id: int) -> Optional[Venta]:
        pass

    @abstractmethod
    def find_by_maquina(self, maquina_id: int) -> List[Venta]:
        pass

    @abstractmethod
    def find_by_fecha_rango(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[Venta]:
        pass

    @abstractmethod
    def save(self, venta: Venta) -> Venta:
        pass

    @abstractmethod
    def get_ventas_por_producto(self, producto_id: int) -> List[Venta]:
        pass

    @abstractmethod
    def get_total_ventas_por_maquina(self, maquina_id: int) -> float:
        pass
    
    # NUEVO: Método para eliminar ventas por producto
    @abstractmethod
    def delete_ventas_por_producto(self, producto_id: int) -> int:
        pass