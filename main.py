import datetime
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import text
from sqlalchemy.orm import Session
from time import time

from app.database import create_db_and_tables, get_session
from app.routers import usuarios, peliculas, favoritos

# Importar la configuración desde app.config
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestor de ciclo de vida de la aplicación.
    Se ejecuta al iniciar y al cerrar la aplicación.
    """
    # Startup: Crear tablas en la base de datos
    create_db_and_tables()
    yield
    
    # Shutdown: Limpiar recursos si es necesario
    print("cerrando aplicación...")


# Crear la instancia de FastAPI con metadatos apropiados
# Incluir: title, description, version, contact, license_info
app = FastAPI(
    title="API de Películas",
    description="API RESTful para gestionar usuarios, películas y favoritos",
    version="1.0.0",
    lifespan=lifespan,
    # Agregar información de contacto y licencia
    contact={
        "name": "Tu Nombre",
        "email": "tu.email@example.com",
    },
    license_info={
        "name": "MIT",
    },
)


# Configurar CORS para permitir solicitudes desde diferentes orígenes
# Esto es importante para desarrollo con frontend separado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir los routers de usuarios, peliculas y favoritos
# Ejemplo:
app.include_router(usuarios.router)
app.include_router(peliculas.router)
app.include_router(favoritos.router)


# Crear un endpoint raíz que retorne información básica de la API
@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raíz de la API.
    Retorna información básica y enlaces a la documentación.
    """
    return {
        # Agregar información 
        "message": "Bienvenido a la API de Películas",
        "version": "1.0.0",
        "documentacion": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "endpoints_principales":  {
            "usuarios": "/api/usuarios",
            "peliculas": "/api/peliculas",
            "favoritos": "/api/favoritos"
        },
        "status": "activo",
        "entorno": settings.environment
    }


# Crear un endpoint de health check para monitoreo
@app.get("/health", tags=["Health"])
async def health_check(db: Session = Depends(get_session)):  # Cambiado de 'dB' a 'db'
    """
    Health check endpoint para verificar el estado de la API.
    Útil para sistemas de monitoreo y orquestación.
    """
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",  # Actualizado para reflejar el estado real
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    
    print(f"{request.method} {request.url} - {response.status_code} - {process_time:.2f}s")
    return response


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        # Configurar el servidor uvicorn con los parámetros apropiados
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
 )