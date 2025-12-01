from typing import List, Optional
from app.domain.repositories.maquina_repository import IMaquinaRepository
from app.domain.entities.maquina import Maquina
from app.infrastructure.schemas.maquina_schema import MaquinaCreate, MaquinaUpdate

class MaquinaUseCase:
    
    def __init__(self, maquina_repository: IMaquinaRepository):
        self.maquina_repository = maquina_repository

    def get_all_maquinas(self) -> List[Maquina]:
        return self.maquina_repository.find_all()

    def get_maquina_by_id(self, maquina_id: int) -> Optional[Maquina]:
        return self.maquina_repository.find_by_id(maquina_id)

    def create_maquina(self, maquina_data: MaquinaCreate) -> Maquina:
        maquina = Maquina(**maquina_data.dict())
        return self.maquina_repository.save(maquina)

    def update_maquina(self, maquina_id: int, maquina_data: MaquinaUpdate) -> Optional[Maquina]:
        maquina = self.maquina_repository.find_by_id(maquina_id)
        if maquina:
            update_data = maquina_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(maquina, key, value)
            return self.maquina_repository.update(maquina)
        return None

    def delete_maquina(self, maquina_id: int) -> bool:
        maquina = self.maquina_repository.find_by_id(maquina_id)
        if maquina:
            self.maquina_repository.delete(maquina_id)
            return True
        return False