from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base

class Marca(Base):
    __tablename__ = "Marcas"

    MarcaID = Column(Integer, primary_key=True, autoincrement=True)
    NombreMarca = Column(String(100), nullable=False)
    PaisOrigen = Column(String(100))

    productos = relationship("Producto", back_populates="marca")
