import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from common.database.database import Base, get_db
from fastapi.testclient import TestClient
from main import app

# Usar la misma DATABASE_URL que en producción
DATABASE_URL = "sqlite:///./test_db.sqlite"  # Asegúrate de que esto coincida con DATABASE_URL en deploy.yml

# Crear el engine y la sesión de prueba
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Crea las tablas antes de ejecutar las pruebas y las elimina después."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    """Proporciona una sesión de base de datos para cada prueba."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db):
    """Proporciona un cliente de prueba que utiliza la sesión de base de datos de prueba."""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()