from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from common.schemas.cuenta import CuentaResponse  # Asegúrate de tener este esquema definido

class UsuarioCreate(BaseModel):
    nombre: str = Field(..., json_schema_extra={"example": "Juan Pérez"})
    email: EmailStr = Field(..., json_schema_extra={"example": "juan.perez@example.com"})
    password: str = Field(..., min_length=8, json_schema_extra={"example": "securepassword"})

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
    nombre: Optional[str] = Field(None, json_schema_extra={"example": "Juan Pérez"})
    email: Optional[EmailStr] = Field(None, json_schema_extra={"example": "juan.nuevo@example.com"})
    password: Optional[str] = Field(None, min_length=8, json_schema_extra={"example": "nueva_securepassword"})
    bio: Optional[str] = Field(None, json_schema_extra={"example": "Actualización de biografía."})
    avatar_url: Optional[str] = Field(None, json_schema_extra={"example": "http://example.com/nuevo_avatar.jpg"})