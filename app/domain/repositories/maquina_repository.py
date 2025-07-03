from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.maquina import Maquina

class IMaquinaRepository(ABC):
    
    @abstractmethod
    def find_all(self) -> List[Maquina]:
        pass

    @abstractmethod
    def find_by_id(self, maquina_id: int) -> Optional[Maquina]:
        pass

    @abstractmethod
    def save(self, maquina: Maquina) -> Maquina:
        pass

    @abstractmethod
    def update(self, maquina: Maquina) -> Maquina:
        pass

    @abstractmethod
    def delete(self, maquina_id: int) -> None:
        pass