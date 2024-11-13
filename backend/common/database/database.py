import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os


# Intentar cargar las variables de entorno desde .env solo si existe
dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
if os.path.exists(dotenv_path):
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=dotenv_path)

# Obtener la URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

# Verificar si se ha cargado correctamente la URL de la base de datos
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL no está definida. Asegúrate de tener un archivo .env correctamente configurado.")


# Verificar si estamos usando SQLite
if 'sqlite' in DATABASE_URL:
    # Configuración para SQLite
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # Configuración para otros motores de base de datos (por ejemplo, PostgreSQL)
    engine = create_engine(
        DATABASE_URL,
        pool_size=20,              # Tamaño del pool de conexiones
        max_overflow=10,           # Conexiones adicionales que se pueden abrir si el pool está lleno
        pool_timeout=30,           # Tiempo de espera máximo para obtener una conexión
        pool_recycle=1800,         # Tiempo de reciclaje de conexiones (en segundos)
        pool_pre_ping=True         # Verifica la conexión antes de usarla
    )


# Crear la sesión de SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


