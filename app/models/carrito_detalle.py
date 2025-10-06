# app/models/carrito_detalle.py
from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from app.db import Base

class CarritoDetalle(Base):
    __tablename__ = "CarritoDetalle"

    CarritoDetalleID = Column(Integer, primary_key=True, autoincrement=True)
    CarritoID = Column(Integer, ForeignKey("Carritos.CarritoID"), nullable=False)
    ProductoID = Column(Integer, ForeignKey("Productos.ProductoID"), nullable=False)
    Cantidad = Column(Integer, nullable=False)
    PrecioUnitario = Column(DECIMAL(10, 2), nullable=False)

    carrito = relationship("Carrito", back_populates="detalles")
    producto = relationship("Producto")
