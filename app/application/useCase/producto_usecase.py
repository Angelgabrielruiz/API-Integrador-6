from typing import List, Optional
from app.domain.repositories.product_repository import IProductoRepository
from app.domain.repositories.venta_repository import IVentaRepository  # NUEVO
from app.domain.entities.producto import Producto
from app.infrastructure.schemas.producto_schema import ProductoCreate, ProductoUpdate
from app.infrastructure.services.cloudinary_service import CloudinaryService

class ProductoUseCase:
    
    def __init__(self, producto_repository: IProductoRepository, venta_repository: IVentaRepository = None):  # MODIFICADO
        self.producto_repository = producto_repository
        self.venta_repository = venta_repository  # NUEVO
        self.cloudinary_service = CloudinaryService()

    def get_all_productos(self) -> List[Producto]:
        return self.producto_repository.find_all()

    def get_producto_by_id(self, producto_id: int) -> Optional[Producto]:
        return self.producto_repository.find_by_id(producto_id)

    def create_producto(self, producto_data: ProductoCreate) -> Producto:
        producto = Producto(**producto_data.dict())
        return self.producto_repository.save(producto)
    
    def create_producto_with_image(self, producto_data: ProductoCreate, url_imagen: Optional[str] = None, public_id_imagen: Optional[str] = None) -> Producto:
        producto_dict = producto_data.dict()
        producto_dict["url_imagen"] = url_imagen
        producto_dict["public_id_imagen"] = public_id_imagen
        
        producto = Producto(**producto_dict)
        return self.producto_repository.save(producto)

    def update_producto(self, producto_id: int, producto_data: ProductoUpdate) -> Optional[Producto]:
        producto = self.producto_repository.find_by_id(producto_id)
        if producto:
            update_data = producto_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(producto, key, value)
            return self.producto_repository.update(producto)
        return None
    
    def update_producto_with_image(self, producto_id: int, producto_data: ProductoUpdate, url_imagen: Optional[str] = None, public_id_imagen: Optional[str] = None) -> Optional[Producto]:
        producto = self.producto_repository.find_by_id(producto_id)
        if producto:
            # Si hay nueva imagen, eliminar la anterior
            if url_imagen and producto.public_id_imagen:
                self.cloudinary_service.delete_image(producto.public_id_imagen)
            
            # Actualizar datos básicos
            update_data = producto_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(producto, key, value)
            
            # Actualizar imagen si se proporciona
            if url_imagen:
                producto.url_imagen = url_imagen
                producto.public_id_imagen = public_id_imagen
            
            return self.producto_repository.update(producto)
        return None

    def delete_producto(self, producto_id: int) -> bool:
        producto = self.producto_repository.find_by_id(producto_id)
        if producto:
            # NUEVO: Eliminar todas las ventas asociadas al producto ANTES de eliminar el producto
            if self.venta_repository:
                ventas_eliminadas = self.venta_repository.delete_ventas_por_producto(producto_id)
                print(f"Se eliminaron {ventas_eliminadas} ventas asociadas al producto '{producto.nombre}'")
            
            # Eliminar imagen de Cloudinary si existe
            if producto.public_id_imagen:
                self.cloudinary_service.delete_image(producto.public_id_imagen)
            
            # Finalmente eliminar el producto
            self.producto_repository.delete(producto_id)
            return True
        return False