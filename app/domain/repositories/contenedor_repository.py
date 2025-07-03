from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.contenedor import Contenedor

class IContenedorRepository(ABC):
    
    @abstractmethod
    def find_all(self) -> List[Contenedor]:
        pass

    @abstractmethod
    def find_by_id(self, contenedor_id: int) -> Optional[Contenedor]:
        pass

    @abstractmethod
    def find_by_maquina_and_producto(self, maquina_id: int, producto_id: int) -> Optional[Contenedor]:
        pass

    @abstractmethod
    def save(self, contenedor: Contenedor) -> Contenedor:
        pass

    @abstractmethod
    def update(self, contenedor: Contenedor) -> Contenedor:
        pass

    @abstractmethod
    def delete(self, contenedor_id: int) -> None:
        pass