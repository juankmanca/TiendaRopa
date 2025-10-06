from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Usuario(Base):
    __tablename__ = "Usuarios"

    UsuarioID = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(255), nullable=False)
    Email = Column(String(255), nullable=False, unique=True)
    Contrasena = Column(String(255), nullable=False)
    Telefono = Column(String(255))
    RolID = Column(Integer, ForeignKey("Roles.RolID"), nullable=False, default=1)

    rol = relationship("Rol")
    cliente = relationship("Cliente", back_populates="usuario", uselist=False)
