from typing import Optional
from app.domain.repositories.balance_repository import IBalanceRepository
from app.domain.entities.balance import Balance

class BalanceUseCase:
    
    def __init__(self, balance_repository: IBalanceRepository):
        self.balance_repository = balance_repository

    def get_balance_maquina(self, maquina_id: int) -> Optional[Balance]:
        return self.balance_repository.find_by_maquina(maquina_id)

    def agregar_credito(self, maquina_id: int, cantidad: float) -> Balance:
        """Agregar crédito cuando se inserta una moneda"""
        return self.balance_repository.agregar_credito(maquina_id, cantidad)

    def validar_y_descontar(self, maquina_id: int, precio_producto: float) -> bool:
        """Validar si hay suficiente crédito y descontarlo"""
        return self.balance_repository.descontar_credito(maquina_id, precio_producto)

    def get_credito_disponible(self, maquina_id: int) -> float:
        """Obtener el crédito disponible de una máquina"""
        balance = self.balance_repository.find_by_maquina(maquina_id)
        return balance.credito_actual if balance else 0.0
    
    # NUEVO: Método para establecer balance directamente
    def modificar_balance(self, maquina_id: int, nuevo_credito: float) -> Balance:
        """Establecer un nuevo valor de crédito directamente"""
        if nuevo_credito < 0:
            raise ValueError("El crédito no puede ser negativo")
        return self.balance_repository.establecer_credito(maquina_id, nuevo_credito)