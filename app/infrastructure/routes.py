from fastapi import APIRouter

# Importa los enrutadores de los controladores
from .controllers import producto_controller, maquina_controller, contenedor_controller, sensor_controller, valvula_controller, venta_controller, balance_controller
from app.infrastructure.controllers import balance_controller

api_router = APIRouter()

# Incluye las rutas de cada módulo
api_router.include_router(producto_controller.router, prefix="/productos", tags=["productos"])
api_router.include_router(maquina_controller.router, prefix="/maquinas", tags=["maquinas"])
api_router.include_router(contenedor_controller.router, prefix="/contenedores", tags=["contenedores"])
api_router.include_router(sensor_controller.router, prefix="/sensores", tags=["sensores"])
api_router.include_router(valvula_controller.router, prefix="/valvulas", tags=["valvulas"])
api_router.include_router(venta_controller.router, prefix="/ventas", tags=["ventas"])  # Nueva ruta
api_router.include_router(balance_controller.router, prefix="/balance", tags=["balance"])