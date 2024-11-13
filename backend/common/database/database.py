import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Cargar las variables de entorno desde .env si existe
dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)

# Obtener la URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

# Verificar si se ha cargado correctamente la URL de la base de datos
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL no está definida. Asegúrate de tener un archivo .env correctamente configurado.")

# Crear el motor asincrónico para bases de datos
if 'sqlite' in DATABASE_URL:
    # Configuración asincrónica para SQLite
    engine = create_async_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # Configuración asincrónica para otros motores de base de datos
    engine = create_async_engine(
        DATABASE_URL,
        pool_size=20,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
        pool_pre_ping=True
    )

# Crear la sesión asincrónica de SQLAlchemy
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)
Base = declarative_base()

# Dependencia para obtener la sesión asincrónica de la base de datos
async def get_db():
    async with SessionLocal() as session:
        yield session
