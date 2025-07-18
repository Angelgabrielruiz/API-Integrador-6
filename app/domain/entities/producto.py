from sqlalchemy import Column, Integer, String, Float
from app.core.db_postgresql import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Float)
    descripcion = Column(String)
    url_imagen = Column(String, nullable=True)  # Nueva columna para la URL de la imagen
    public_id_imagen = Column(String, nullable=True)  # Para poder eliminar la imagen de Cloudinary