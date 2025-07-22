from fastapi import APIRouter

# Importa los enrutadores de los controladores
from .controllers import producto_controller, maquina_controller, contenedor_controller, sensor_controller, valvula_controller

api_router = APIRouter()

# Incluye las rutas de cada módulo
api_router.include_router(producto_controller.router, prefix="/productos", tags=["productos"])
api_router.include_router(maquina_controller.router, prefix="/maquinas", tags=["maquinas"])
api_router.include_router(contenedor_controller.router, prefix="/contenedores", tags=["contenedores"])
api_router.include_router(sensor_controller.router, prefix="/sensores", tags=["sensores"])
api_router.include_router(valvula_controller.router, prefix="/valvulas", tags=["valvulas"])  # Nueva ruta