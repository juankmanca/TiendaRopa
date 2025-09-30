from sqlalchemy import Column, Integer, String, ForeignKey
from app.db import Base

class Usuario(Base):
    __tablename__ = "Usuarios"

    UsuarioID = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(255), nullable=False)
    Email = Column(String(255), nullable=False, unique=True)
    Contrasena = Column(String(255), nullable=False)
    Telefono = Column(String(50))
    RolID = Column(Integer, ForeignKey("Roles.RolID"), nullable=False)
