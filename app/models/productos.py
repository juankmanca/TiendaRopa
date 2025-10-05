from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Producto(Base):
    __tablename__ = "Productos"

    ProductoID = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(255), nullable=False)
    Descripcion = Column(String(500))
    Precio = Column(DECIMAL(10, 2), nullable=False)
    Stock = Column(Integer, nullable=False)
    CategoriaID = Column(Integer, ForeignKey("Categorias.CategoriaID"), nullable=False)
    MarcaID = Column(Integer, ForeignKey("Marcas.MarcaID"), nullable=False)

    # ✅ Referencia al nombre de la clase, no al nombre de la tabla
    categoria = relationship("Categoria", back_populates="productos")
    marca = relationship("Marca", back_populates="productos")
