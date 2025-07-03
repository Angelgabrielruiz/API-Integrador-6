from typing import List, Optional
from app.domain.repositories.product_repository import IProductoRepository
from app.domain.entities.producto import Producto
from app.infraestructure.schemas.producto_schema import ProductoCreate, ProductoUpdate

class ProductoUseCase:
    
    def __init__(self, producto_repository: IProductoRepository):
        self.producto_repository = producto_repository

    def get_all_productos(self) -> List[Producto]:
        return self.producto_repository.find_all()

    def get_producto_by_id(self, producto_id: int) -> Optional[Producto]:
        return self.producto_repository.find_by_id(producto_id)

    def create_producto(self, producto_data: ProductoCreate) -> Producto:
        producto = Producto(**producto_data.dict())
        return self.producto_repository.save(producto)

    def update_producto(self, producto_id: int, producto_data: ProductoUpdate) -> Optional[Producto]:
        producto = self.producto_repository.find_by_id(producto_id)
        if producto:
            update_data = producto_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(producto, key, value)
            return self.producto_repository.update(producto)
        return None

    def delete_producto(self, producto_id: int) -> bool:
        producto = self.producto_repository.find_by_id(producto_id)
        if producto:
            self.producto_repository.delete(producto_id)
            return True
        return False