from __future__ import annotations  # Permite referencias tipo string
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from services.user_service.schemas import CuentaResponse

class UsuarioCreate(BaseModel):
    nombre: str = Field(..., example="Juan Pérez")
    email: EmailStr = Field(..., example="juan.perez@example.com")
    password: str = Field(..., min_length=8, example="securepassword")
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres.')
        # Puedes añadir más validaciones de fortaleza aquí
        return v

class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre: str
    email: EmailStr
    bio: Optional[str]
    avatar_url: Optional[str]
    fecha_registro: datetime
    fecha_actualizacion_perfil: datetime
    cuenta: CuentaResponse

    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, example="Juan Pérez")
    email: Optional[EmailStr] = Field(None, example="juan.nuevo@example.com")
    password: Optional[str] = Field(None, min_length=8, example="nueva_securepassword")
    bio: Optional[str] = Field(None, example="Actualización de biografía.")
    avatar_url: Optional[str] = Field(None, example="http://example.com/nuevo_avatar.jpg")

    @validator('password')
    def password_strength(cls, v):
        if v and len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres.')
        # Puedes añadir más validaciones de fortaleza aquí
        return v