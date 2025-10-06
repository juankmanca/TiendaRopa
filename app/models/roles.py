from sqlalchemy import Column, Integer, String
from app.db import Base

class Rol(Base):
    __tablename__ = "Roles"

    RolID = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(255), nullable=False)
