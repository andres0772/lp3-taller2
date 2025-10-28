"""
Configuración de la aplicación.
Maneja diferentes entornos: desarrollo, pruebas y producción.
"""

from pydantic_settings import BaseSettings
from typing import Literal
from pydantic import validator

class Settings(BaseSettings):
    """
    Configuración de la aplicación usando Pydantic Settings.
    Lee las variables de entorno desde el archivo .env
    """
    
    # Configuración básica de la aplicación
    app_name: str = "API de Películas"
    app_version: str = "1.0.0"
    debug: bool = False
   
    environment: Literal["development", "testing", "production"] = "development"
    
    
    database_url: str = "sqlite:///./peliculas.db"
    
    # Configuración del servidor
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True # permite recargar automaticamente en desarrollo

    # Configuración de CORS
    # En desarrollo puedes usar ["*"], en producción especifica los orígenes permitidos
    cors_origins: list[str] = ["*"]
    
    #  Configuración de seguridad (para futuras mejoras)
    secret_key: str = "your-secret-key-here"  # Cambiar en producción
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Configuración de logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(levelname)s - %(message)s - %(message)s"
    log_date_format: str = "%Y-%m-%d %H:%M:%S"
    
    class Config:
        """
        Configuración de Pydantic Settings.
        """
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
        # Opcional - Agregar validación personalizada
        @validator("database_url")
        def validate_database_url(cls, v):
            if not v:
                raise ValueError("DATABASE_URL no puede estar vacío")
            return v


# Crear una instancia global de Settings
settings = Settings()


# Opcional - Crear diferentes configuraciones para cada entorno
class DevelopmentSettings(Settings):
    """Configuración para el entorno de desarrollo."""
    debug: bool = True
    environment: Literal["development"] = "development"
    reload: bool = True
    log_level: str = "DEBUG"
    database_url: str = "sqlite:///./peliculas.db"
    cors_origins: list[str] = ["*"]

class TestingSettings(Settings):
    """Configuración para el entorno de pruebas."""
    environment: Literal["testing"] = "testing"
    debug: bool = False
    log_level: str = "DEBUG"
    database_url: str = "sqlite:///./test_peliculas.db"
    cors_origins: list[str] = ["*"]


class ProductionSettings(Settings):
    """Configuración para el entorno de producción."""
    debug: bool = False
    environment: Literal["production"] = "production"
    reload: bool = False
    log_level: str = "WARNING"
    database_url: str = "sqlite:///./peliculas.db"
    cors_origins: list[str] = ["*"]



def get_settings() -> Settings:
    """
    Retorna la configuración apropiada según el entorno.
    """
    env = settings.environment.lower().strip()
    
    if env == "testing":
        return TestingSettings()
    elif env == "production":
        return ProductionSettings()
    else:
        return DevelopmentSettings()



def validate_settings():
    """Valida que todas las configuraciones necesarias estén presentes."""
    required_settings = ["database_url", "app_name"]
    for setting in required_settings:
        if not getattr(settings, setting, None):
            raise ValueError(f"Configuración requerida no encontrada: {setting}")

