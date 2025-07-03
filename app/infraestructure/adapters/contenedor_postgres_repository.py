from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities.contenedor import Contenedor
from app.domain.repositories.contenedor_repository import IContenedorRepository

class ContenedorPostgresRepository(IContenedorRepository):

    def __init__(self, db_session: Session):
        self.db = db_session

    def find_all(self) -> List[Contenedor]:
        return self.db.query(Contenedor).all()

    def find_by_id(self, contenedor_id: int) -> Optional[Contenedor]:
        return self.db.query(Contenedor).filter(Contenedor.id_contenedor == contenedor_id).first()

    def find_by_maquina_and_producto(self, maquina_id: int, producto_id: int) -> Optional[Contenedor]:
        return self.db.query(Contenedor).filter(
            Contenedor.id_maquina == maquina_id, 
            Contenedor.id_producto == producto_id
        ).first()

    def save(self, contenedor_data: Contenedor) -> Contenedor:
        self.db.add(contenedor_data)
        self.db.commit()
        self.db.refresh(contenedor_data)
        return contenedor_data

    def update(self, contenedor: Contenedor) -> Contenedor:
        self.db.commit()
        self.db.refresh(contenedor)
        return contenedor

    def delete(self, contenedor_id: int) -> None:
        contenedor = self.find_by_id(contenedor_id)
        if contenedor:
            self.db.delete(contenedor)
            self.db.commit()