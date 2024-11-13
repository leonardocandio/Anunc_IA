def test_register_usuario(client):
    test_user = {
        "email": "testuser@example.com",
        "nombre": "Usuario Test",
        "password": "securepassword"
    }
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user["email"]
    assert "id_usuario" in data
    assert "cuenta" in data
    assert data["cuenta"]["tipo_cuenta"] == "Standard"
    assert data["cuenta"]["saldo"] == 0.0

def test_register_usuario_email_existente(client):
    test_user = {
        "email": "testuser@example.com",
        "nombre": "Usuario Test 2",
        "password": "securepassword2"
    }
    # Intentar registrar el mismo usuario nuevamente
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "El email ya está registrado."