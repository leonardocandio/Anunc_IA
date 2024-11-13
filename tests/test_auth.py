from fastapi.testclient import TestClient
from backend.main import app
import pytest

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