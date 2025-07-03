from fastapi import FastAPI

# Importaciones de la Arquitectura
from app.core import db_postgresql as database
from app.infraestructure import routes
from app.domain.entities.maquina import Maquina
from app.domain.entities.producto import Producto # Ensure Producto is also imported
from app.domain.entities.contenedor import Contenedor # <-- ADD THIS LINE

# Crea las tablas en la base de datos al iniciar (si no existen)
database.create_db_and_tables()

app = FastAPI(
    title="API Nutribox",
    version="1.0.0"
)

# --- Inclusión de Rutas ---
app.include_router(routes.api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"status": "API Nutribox is running!"}