from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.db.connection import Base


class Category(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    descripcion = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    productos = relationship("Producto", back_populates="categoria")
