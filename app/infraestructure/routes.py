from fastapi import APIRouter
from .controllers import producto_controller, maquina_controller, contenedor_controller

api_router = APIRouter()

# Incluimos las rutas del controlador de productos
api_router.include_router(producto_controller.router, prefix="/productos", tags=["Productos"])

# Incluimos las rutas del controlador de máquinas
api_router.include_router(maquina_controller.router, prefix="/maquinas", tags=["Maquinas"])

# Incluimos las rutas del controlador de contenedores
api_router.include_router(contenedor_controller.router, prefix="/contenedores", tags=["Contenedores"])