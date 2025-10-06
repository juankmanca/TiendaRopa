# app/models/cliente.py
from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db import Base

class Cliente(Base):
    __tablename__ = "Clientes"

    ClienteID = Column(Integer, primary_key=True, autoincrement=True)
    UsuarioID = Column(Integer, ForeignKey("Usuarios.UsuarioID"), nullable=False)
    FechaRegistro = Column(DateTime, default=func.now())
    Estado = Column(Boolean, default=True)

    usuario = relationship("Usuario", back_populates="cliente")
    carritos = relationship("Carrito", back_populates="cliente", cascade="all, delete-orphan")
