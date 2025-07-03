from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.producto import Producto

class IProductoRepository(ABC):
    
    @abstractmethod
    def find_all(self) -> List[Producto]:
        pass

    @abstractmethod
    def find_by_id(self, producto_id: int) -> Optional[Producto]:
        pass

    @abstractmethod
    def save(self, producto: Producto) -> Producto:
        pass

    @abstractmethod
    def update(self, producto: Producto) -> Producto:
        pass

    @abstractmethod
    def delete(self, producto_id: int) -> None:
        pass