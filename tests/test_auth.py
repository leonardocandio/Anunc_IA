import pytest
from httpx import AsyncClient
from backend.main import app
from backend.common.database.database import engine, get_db, Base  # Asegúrate de importar `Base`
from backend.common.models.usuario import Usuario  # importa cualquier modelo necesario

@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    # Crea las tablas en la base de datos antes de las pruebas
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Elimina las tablas al finalizar las pruebas (opcional)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

@pytest.fixture
def test_db_session():
    db = next(get_db())
    yield db
    db.rollback()

@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post("/auth/register", json={
        "nombre": "Test User",
        "email": "test.user@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test.user@example.com"

@pytest.mark.asyncio
async def test_login_user(client):
    response = await client.post("/auth/login", data={
        "username": "test.user@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Inicio de sesión exitoso"
    assert "session_id" in response.cookies

@pytest.mark.asyncio
async def test_check_session(client):
    # Primero inicia sesión para obtener una sesión válida
    login_response = await client.post("/auth/login", data={
        "username": "test.user@example.com",
        "password": "securepassword"
    })
    session_id = login_response.cookies.get("session_id")
    assert session_id is not None

    # Prueba de verificación de sesión
    response = await client.get("/auth/check_session", cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json()["message"] == "Sesión válida"

@pytest.mark.asyncio
async def test_logout_user(client):
    # Inicia sesión para tener una sesión activa
    login_response = await client.post("/auth/login", data={
        "username": "test.user@example.com",
        "password": "securepassword"
    })
    session_id = login_response.cookies.get("session_id")
    assert session_id is not None

    # Cerrar sesión
    logout_response = await client.post("/auth/logout", cookies={"session_id": session_id})
    assert logout_response.status_code == 200
    assert logout_response.json()["message"] == "Sesión cerrada"

    # Verificar que la sesión ya no es válida
    check_session_response = await client.get("/auth/check_session", cookies={"session_id": session_id})
    assert check_session_response.status_code == 401