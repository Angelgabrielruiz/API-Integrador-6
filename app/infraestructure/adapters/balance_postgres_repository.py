from typing import Optional
from sqlalchemy.orm import Session
from app.domain.entities.balance import Balance
from app.domain.repositories.balance_repository import IBalanceRepository

class BalancePostgresRepository(IBalanceRepository):

    def __init__(self, db_session: Session):
        self.db = db_session

    def find_by_maquina(self, maquina_id: int) -> Optional[Balance]:
        return self.db.query(Balance).filter(Balance.id_maquina == maquina_id).first()

    def save(self, balance: Balance) -> Balance:
        self.db.add(balance)
        self.db.commit()
        self.db.refresh(balance)
        return balance

    def update(self, balance: Balance) -> Balance:
        self.db.commit()
        self.db.refresh(balance)
        return balance

    def agregar_credito(self, maquina_id: int, cantidad: float) -> Balance:
        balance = self.find_by_maquina(maquina_id)
        if not balance:
            # Crear balance si no existe
            balance = Balance(id_maquina=maquina_id, credito_actual=cantidad)
            return self.save(balance)
        else:
            balance.credito_actual += cantidad
            return self.update(balance)

    def descontar_credito(self, maquina_id: int, cantidad: float) -> bool:
        balance = self.find_by_maquina(maquina_id)
        if not balance or balance.credito_actual < cantidad:
            return False
        
        balance.credito_actual -= cantidad
        self.update(balance)
        return True
    
    # NUEVO: Método para establecer balance directamente
    def establecer_credito(self, maquina_id: int, nuevo_credito: float) -> Balance:
        balance = self.find_by_maquina(maquina_id)
        if not balance:
            # Crear balance si no existe
            balance = Balance(id_maquina=maquina_id, credito_actual=nuevo_credito)
            return self.save(balance)
        else:
            balance.credito_actual = nuevo_credito
            return self.update(balance)