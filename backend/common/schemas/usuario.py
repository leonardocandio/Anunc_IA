from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from common.schemas.cuenta import CuentaResponse  # Asegúrate de tener este esquema definido

class UsuarioCreate(BaseModel):
    nombre: str = Field(..., example="Juan Pérez")
    email: EmailStr = Field(..., example="juan.perez@example.com")
    password: str = Field(..., min_length=8, example="securepassword")

class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre: str
    email: EmailStr
    bio: Optional[str]
    avatar_url: Optional[str]
    fecha_registro: datetime
    fecha_actualizacion_perfil: datetime
    cuenta: Optional[CuentaResponse]  # Usa el esquema directamente

    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, example="Juan Pérez")
    email: Optional[EmailStr] = Field(None, example="juan.nuevo@example.com")
    password: Optional[str] = Field(None, min_length=8, example="nueva_securepassword")
    bio: Optional[str] = Field(None, example="Actualización de biografía.")
    avatar_url: Optional[str] = Field(None, example="http://example.com/nuevo_avatar.jpg")