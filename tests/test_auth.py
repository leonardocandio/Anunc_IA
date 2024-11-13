import pytest
from httpx import AsyncClient
from backend.main import app
from backend.common.database.database import get_db
from backend.common.models.usuario import Usuario

@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

@pytest.fixture
def test_db_session():
    # Configura aquí una sesión de prueba para la base de datos si necesitas aislar datos de prueba
    db = next(get_db())
    yield db
    db.rollback()

async def test_register_user(async_client):
    response = await async_client.post("/auth/register", json={
        "nombre": "Test User",
        "email": "test.user@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test.user@example.com"

async def test_login_user(async_client):
    response = await async_client.post("/auth/login", data={
        "username": "test.user@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Inicio de sesión exitoso"
    assert "session_id" in response.cookies

async def test_check_session(async_client):
    # Primero inicia sesión para obtener una sesión válida
    login_response = await async_client.post("/auth/login", data={
        "username": "test.user@example.com",
        "password": "securepassword"
    })
    session_id = login_response.cookies.get("session_id")
    assert session_id is not None

    # Prueba de verificación de sesión
    response = await async_client.get("/auth/check_session", cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json()["message"] == "Sesión válida"

async def test_logout_user(async_client):
    # Inicia sesión para tener una sesión activa
    login_response = await async_client.post("/auth/login", data={
        "username": "test.user@example.com",
        "password": "securepassword"
    })
    session_id = login_response.cookies.get("session_id")
    assert session_id is not None

    # Cerrar sesión
    logout_response = await async_client.post("/auth/logout", cookies={"session_id": session_id})
    assert logout_response.status_code == 200
    assert logout_response.json()["message"] == "Sesión cerrada"

    # Verificar que la sesión ya no es válida
    check_session_response = await async_client.get("/auth/check_session", cookies={"session_id": session_id})
    assert check_session_response.status_code == 401