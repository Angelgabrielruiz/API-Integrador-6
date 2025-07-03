from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities.producto import Producto
from app.domain.repositories.product_repository import IProductoRepository

class ProductoPostgresRepository(IProductoRepository):

    def __init__(self, db_session: Session):
        self.db = db_session

    def find_all(self) -> List[Producto]:
        return self.db.query(Producto).all()

    def find_by_id(self, producto_id: int) -> Optional[Producto]:
        return self.db.query(Producto).filter(Producto.id == producto_id).first()

    def save(self, producto_data: Producto) -> Producto:
        self.db.add(producto_data)
        self.db.commit()
        self.db.refresh(producto_data)
        return producto_data

    def update(self, producto: Producto) -> Producto:
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def delete(self, producto_id: int) -> None:
        producto = self.find_by_id(producto_id)
        if producto:
            self.db.delete(producto)
            self.db.commit()