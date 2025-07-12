from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database_deps import get_db_session  # Agregar esta línea

from app.core import db_postgresql as database
from app.infraestructure.adapters.producto_postgres_repository import ProductoPostgresRepository
from app.domain.repositories.product_repository import IProductoRepository
from app.application.useCase.producto_usecase import ProductoUseCase

# Importaciones para Maquina
from app.infraestructure.adapters.maquina_postgres_repository import MaquinaPostgresRepository
from app.domain.repositories.maquina_repository import IMaquinaRepository
from app.application.useCase.maquina_usecase import MaquinaUseCase

# Importaciones para Contenedor
from app.infraestructure.adapters.contenedor_postgres_repository import ContenedorPostgresRepository
from app.domain.repositories.contenedor_repository import IContenedorRepository
from app.application.useCase.contenedor_usecase import ContenedorUseCase

# Importaciones para SensorReading
from app.infraestructure.adapters.sensor_reading_postgres_repository import SensorReadingPostgresRepository
from app.domain.repositories.sensor_reading_repository import ISensorReadingRepository
from app.application.useCase.sensor_usecase import SensorUseCase

# Importaciones para Usuario y Auth
from app.infraestructure.adapters.usuario_postgres_repository import UsuarioPostgresRepository
from app.domain.repositories.usuario_repository import IUsuarioRepository
from app.application.useCase.auth_usecase import AuthUseCase

def get_producto_repository(db: Session = Depends(get_db_session)) -> IProductoRepository:
    return ProductoPostgresRepository(db)

def get_producto_use_case(repo: IProductoRepository = Depends(get_producto_repository)) -> ProductoUseCase:
    return ProductoUseCase(repo)

# --- Dependencias para Maquina ---

def get_maquina_repository(db: Session = Depends(get_db_session)) -> IMaquinaRepository:
    return MaquinaPostgresRepository(db)

def get_maquina_use_case(repo: IMaquinaRepository = Depends(get_maquina_repository)) -> MaquinaUseCase:
    return MaquinaUseCase(repo)

# --- Dependencias para Contenedor ---

def get_contenedor_repository(db: Session = Depends(get_db_session)) -> IContenedorRepository:
    return ContenedorPostgresRepository(db)

def get_contenedor_use_case(repo: IContenedorRepository = Depends(get_contenedor_repository)) -> ContenedorUseCase:
    return ContenedorUseCase(repo)

# --- Dependencias para SensorReading ---

def get_sensor_reading_repository(db: Session = Depends(get_db_session)) -> ISensorReadingRepository:
    return SensorReadingPostgresRepository(db)

def get_sensor_use_case(repo: ISensorReadingRepository = Depends(get_sensor_reading_repository)) -> SensorUseCase:
    return SensorUseCase(repo)

# --- Dependencias para Usuario y Auth ---

def get_usuario_repository(db: Session = Depends(get_db_session)) -> IUsuarioRepository:
    return UsuarioPostgresRepository(db)

def get_auth_use_case(repo: IUsuarioRepository = Depends(get_usuario_repository)) -> AuthUseCase:
    return AuthUseCase(repo)
