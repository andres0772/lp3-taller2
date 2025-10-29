"""
Configuración de la base de datos y gestión de sesiones.
Utiliza SQLModel para ORM y gestión de conexiones.
"""

from sqlalchemy import text
from sqlmodel import SQLModel, create_engine, Session, select
from typing import Generator
from app.models import Usuario, Pelicula, Favorito
from app.config import settings


engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # Muestra las consultas SQL en consola si debug=True
    connect_args={"check_same_thread": False},  # Necesario para SQLite
)


# Función para crear todas las tablas
def create_db_and_tables():
    """
    Crea todas las tablas en la base de datos.
    Se llama al iniciar la aplicación.
    """

    SQLModel.metadata.create_all(engine)
    print("Tablas de la base de datos creadas correctamente")


# Función para eliminar todas las tablas (útil para testing)
def drop_db_and_tables():
    """
    Elimina todas las tablas de la base de datos.
    Usar con precaución - elimina todos los datos.
    """
    SQLModel.metadata.drop_all(engine)
    print("Tablas de la base de datos eliminadas")


# Obtener una sesión de base de datos
def get_session() -> Generator[Session, None, None]:
    """
    Generador de sesiones de base de datos.
    Se usa como dependencia en los endpoints de FastAPI.

    Uso en endpoints:
        @app.get("/items")
        def read_items(session: Session = Depends(get_session)):
            items = session.exec(select(Item)).all()
            return items
    """
    with Session(engine) as session:
        yield session



def check_database_connection() -> bool:
    """
    Verifica que la conexión a la base de datos funcione correctamente.
    Retorna True si la conexión es exitosa, False en caso contrario.
    """
    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1")).one()
            print("Conexión a la base de datos exitosa")
            return True
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        return False


class DatabaseSession:
    """
    Context manager para manejar sesiones de base de datos.
    Útil para operaciones fuera de endpoints FastAPI.

    Uso:
        with DatabaseSession() as session:
            user = session.get(Usuario, user_id)
    """

    def __enter__(self) -> Session:
        self.session = Session(engine)
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.session.rollback()
        self.session.close()


def init_sample_data():
    with Session(engine) as session:
        # 1. Verificar si ya hay datos
        if session.exec(select(Usuario)).first():
            print("⚠️  Ya hay datos. No se agregarán más.")
            return

        print("📝 Inicializando datos de prueba...")

        # 2. Crear datos de ejemplo
        usuarios = [
            Usuario(nombre="Ana", correo="ana@ejemplo.com"),
            Usuario(nombre="Carlos", correo="carlos@ejemplo.com"),
        ]
        peliculas = [
            Pelicula(titulo="El Padrino", genero="Drama", año=1972),
            Pelicula(titulo="El Señor de los Anillos", genero="Fantasía", año=2001),
        ]
        favoritos = [
            Favorito(usuario_id=1, pelicula_id=1),
            Favorito(usuario_id=1, pelicula_id=2),
            Favorito(usuario_id=2, pelicula_id=2),
        ]

        # 3. Guardar todo
        session.add_all(usuarios + peliculas + favoritos)
        session.commit()
        print("✅ Datos creados exitosamente")
