from pydantic import BaseModel
from datetime import datetime

class CuentaResponse(BaseModel):
    id_cuenta: int
    tipo_cuenta: str
    saldo: float
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True