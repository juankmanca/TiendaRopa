from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db import Base

class Categoria(Base):
    __tablename__ = "Categorias"

    CategoriaID = Column(Integer, primary_key=True, autoincrement=True)
    NombreCategoria = Column(String(100), nullable=False)
    Descripcion = Column(Text)

    productos = relationship("Producto", back_populates="categoria")
