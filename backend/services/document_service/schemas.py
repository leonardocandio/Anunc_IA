from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DocumentoCreate(BaseModel):
    tipo_documento: str = Field(..., example="Informe")
    contenido: str = Field(..., example="Contenido del documento...")

class DocumentoUpdate(BaseModel):
    tipo_documento: Optional[str] = Field(None, example="Reporte")
    contenido: Optional[str] = Field(None, example="Contenido actualizado del documento...")

class DocumentoResponse(BaseModel):
    id_documento: int
    tipo_documento: str
    contenido: str
    fecha_creacion: datetime
    id_usuario: int

    class Config:
        from_attributes = True
