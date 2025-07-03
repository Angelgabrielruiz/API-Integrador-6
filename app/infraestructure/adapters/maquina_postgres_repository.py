from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities.maquina import Maquina
from app.domain.repositories.maquina_repository import IMaquinaRepository

class MaquinaPostgresRepository(IMaquinaRepository):

    def __init__(self, db_session: Session):
        self.db = db_session

    def find_all(self) -> List[Maquina]:
        return self.db.query(Maquina).all()

    def find_by_id(self, maquina_id: int) -> Optional[Maquina]:
        return self.db.query(Maquina).filter(Maquina.id_maquina == maquina_id).first()

    def save(self, maquina_data: Maquina) -> Maquina:
        self.db.add(maquina_data)
        self.db.commit()
        self.db.refresh(maquina_data)
        return maquina_data

    def update(self, maquina: Maquina) -> Maquina:
        self.db.commit()
        self.db.refresh(maquina)
        return maquina

    def delete(self, maquina_id: int) -> None:
        maquina = self.find_by_id(maquina_id)
        if maquina:
            self.db.delete(maquina)
            self.db.commit()