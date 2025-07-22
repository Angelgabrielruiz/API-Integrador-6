from typing import List, Optional
from app.domain.repositories.contenedor_repository import IContenedorRepository
from app.domain.entities.contenedor import Contenedor
from app.infraestructure.schemas.contenedor_schema import ContenedorCreate, ContenedorUpdate, DispensarRequest

class ContenedorUseCase:
    
    def __init__(self, contenedor_repository: IContenedorRepository):
        self.contenedor_repository = contenedor_repository

    def get_all_contenedores(self) -> List[Contenedor]:
        return self.contenedor_repository.find_all()

    def get_contenedor_by_id(self, contenedor_id: int) -> Optional[Contenedor]:
        return self.contenedor_repository.find_by_id(contenedor_id)

    def create_contenedor(self, contenedor_data: ContenedorCreate) -> Contenedor:
        contenedor = Contenedor(**contenedor_data.dict())
        return self.contenedor_repository.save(contenedor)

    def get_contenedor_by_maquina_and_producto(self, maquina_id: int, producto_id: int) -> Optional[Contenedor]:
        return self.contenedor_repository.find_by_maquina_and_producto(maquina_id, producto_id)

    def dispensar_producto(self, dispensar_data: DispensarRequest) -> Optional[Contenedor]:
        contenedor = self.contenedor_repository.find_by_maquina_and_producto(
            maquina_id=dispensar_data.id_maquina,
            producto_id=dispensar_data.id_producto
        )

        if not contenedor:
            return None # Or raise a specific exception

        if contenedor.cantidad_actual < dispensar_data.cantidad_dispensada:
            # Not enough product, you could raise an exception here to give more specific feedback
            raise ValueError("Cantidad insuficiente en el contenedor.")

        contenedor.cantidad_actual -= dispensar_data.cantidad_dispensada
        return self.contenedor_repository.update(contenedor)

    def update_contenedor(self, contenedor_id: int, contenedor_data: ContenedorUpdate) -> Optional[Contenedor]:
        contenedor = self.contenedor_repository.find_by_id(contenedor_id)
        if contenedor:
            update_data = contenedor_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(contenedor, key, value)
            return self.contenedor_repository.update(contenedor)
        return None

    def delete_contenedor(self, contenedor_id: int) -> bool:
        contenedor = self.contenedor_repository.find_by_id(contenedor_id)
        if contenedor:
            self.contenedor_repository.delete(contenedor_id)
            return True
        return False