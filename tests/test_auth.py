import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app  # Importa tu aplicación principal desde el archivo adecuado
from common.database.database import Base, get_db
from common.schemas.usuario import UsuarioCreate

# Configuración de base de datos de prueba en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # Usa SQLite en memoria para pruebas rápidas
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas en la base de datos de prueba
Base.metadata.create_all(bind=engine)

# Dependencia de base de datos para las pruebas
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Crear cliente de prueba
client = TestClient(app)

@pytest.fixture
def test_user():
    # Datos de prueba para el usuario
    return {
        "nombre": "Usuario Test",
        "email": "testuser@example.com",
        "password": "securepassword"
    }

def test_register_usuario(test_user):
    # Realizar solicitud POST al endpoint de registro
    response = client.post("/auth/register", json=test_user)

    # Aserciones para verificar que el registro fue exitoso
    assert response.status_code == 201  # Código de estado esperado
    data = response.json()
    assert data["nombre"] == test_user["nombre"]
    assert data["email"] == test_user["email"]
    assert "id_usuario" in data  # Verificar que se devuelve un id de usuario