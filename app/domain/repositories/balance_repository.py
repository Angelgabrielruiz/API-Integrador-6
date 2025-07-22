from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.balance import Balance

class IBalanceRepository(ABC):
    
    @abstractmethod
    def find_by_maquina(self, maquina_id: int) -> Optional[Balance]:
        pass

    @abstractmethod
    def save(self, balance: Balance) -> Balance:
        pass

    @abstractmethod
    def update(self, balance: Balance) -> Balance:
        pass

    @abstractmethod
    def agregar_credito(self, maquina_id: int, cantidad: float) -> Balance:
        pass

    @abstractmethod
    def descontar_credito(self, maquina_id: int, cantidad: float) -> bool:
        pass
    
    # NUEVO: Método para establecer balance directamente
    @abstractmethod
    def establecer_credito(self, maquina_id: int, nuevo_credito: float) -> Balance:
        pass