from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from common.database.database import Base
from datetime import datetime, timezone

class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {'extend_existing': True}

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    contraseña = Column(String, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    bio = Column(Text, nullable=True)
    avatar_url = Column(String, nullable=True)
    fecha_actualizacion_perfil = Column(DateTime, default=datetime.now(timezone.utc), nullable=False, onupdate=datetime.now(timezone.utc))

    # Modificación aquí: especifica la referencia de cuenta
    cuenta = relationship("common.models.usuario.Cuenta", uselist=False, back_populates="usuario")

    # Relación Uno a Muchos con Documento
    documentos = relationship("Documento", back_populates="usuario", cascade="all, delete-orphan")

    # Relación Uno a Muchos con Producto
    productos = relationship("Producto", back_populates="usuario", cascade="all, delete-orphan")

class Cuenta(Base):
    __tablename__ = "cuentas"
    __table_args__ = {'extend_existing': True}  # Añadir esta línea

    id_cuenta = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), unique=True, nullable=False)
    tipo_cuenta = Column(String, nullable=False, default="Standard")
    saldo = Column(Float, default=0.0, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    fecha_actualizacion = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False
    )

    # Modificación aquí: asegúrate de que la referencia sea específica
    usuario = relationship("common.models.usuario.Usuario", back_populates="cuenta")