from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from services.auth_service import security, schemas
from common.database.database import get_db
from datetime import timedelta
from common.models.usuario import Usuario, Cuenta
from common.schemas.usuario import UsuarioCreate, UsuarioResponse
from common.utils.session_manager import SessionManager  # Importar SessionManager


router = APIRouter()
session_manager = SessionManager()  # Inicializar el gestor de sesiones

import traceback

@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, summary="Registrar un nuevo usuario")
async def register_usuario(usuario: UsuarioCreate, response: Response, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="El email ya está registrado.")

    try:
        # Paso 1: Crear el usuario con campos básicos
        hashed_password = security.get_password_hash(usuario.password)
        nuevo_usuario = Usuario(
            nombre=usuario.nombre,
            email=usuario.email,
            contraseña=hashed_password
        )
        print("Usuario creado en memoria")

        # Paso 2: Crear una cuenta asociada con valores predeterminados
        nueva_cuenta = Cuenta(
            tipo_cuenta="Standard",
            saldo=0.0
        )
        nuevo_usuario.cuenta = nueva_cuenta
        print("Cuenta asociada creada")

        # Paso 3: Añadir y confirmar en la base de datos
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        print("Usuario y cuenta guardados en la base de datos")

        # Paso 4: Generar un token JWT
        access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            data={"sub": nuevo_usuario.email}, expires_delta=access_token_expires
        )
        print("Token JWT generado")

        # Paso 5: Almacenar el JWT en Redis
        session_id = f"session_{nuevo_usuario.email}"
        await session_manager.store_jwt(session_id, access_token)
        print("Token JWT almacenado en Redis")

        # Paso 6: Configurar la cookie con el session_id
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,  # Mejorar la seguridad
            samesite="Lax",
            secure=False  # Cambiar a True en producción con HTTPS
        )
        print("Cookie de sesión configurada en la respuesta")

        return nuevo_usuario
    except Exception as e:
        db.rollback()
        print(f"Error en register_usuario: {e}")
        traceback.print_exc()  # Imprime el traceback completo
        raise HTTPException(status_code=500, detail="Error al registrar el usuario.")

@router.post("/login", summary="Iniciar sesión de un usuario")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = security.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credenciales inválidas.",
        )

    # Generar el token JWT
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    # Almacenar el JWT en Redis con una clave de sesión
    session_id = f"session_{user.email}"
    await session_manager.store_jwt(session_id, access_token)

    # Configurar la cookie con el session_id
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=False,
        samesite="Lax",
        secure=False  # Cambiar a True en producción con HTTPS
    )

    return {"message": "Inicio de sesión exitoso"}

@router.post("/logout", summary="Cerrar sesión")
async def logout(response: Response, request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        await session_manager.delete_jwt(session_id)  # Eliminar el JWT de Redis
        response.delete_cookie("session_id")          # Eliminar la cookie de sesión
    return {"message": "Sesión cerrada"}

@router.get("/check_session", summary="Verificar sesión")
async def check_session(current_user: Usuario = Depends(security.get_current_user)):
    return {"message": "Sesión válida", "user": current_user.email}
