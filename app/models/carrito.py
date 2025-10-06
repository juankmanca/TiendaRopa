# app/models/carrito.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from app.db import Base

class Carrito(Base):
    __tablename__ = "Carritos"

    CarritoID = Column(Integer, primary_key=True, autoincrement=True)
    ClienteID = Column(Integer, ForeignKey("Clientes.ClienteID"), nullable=False)
    FechaCreacion = Column(DateTime, default=func.now())
    Activo = Column(Boolean, default=True)

    cliente = relationship("Cliente", back_populates="carritos")
    detalles = relationship("CarritoDetalle", back_populates="carrito", cascade="all, delete-orphan")
