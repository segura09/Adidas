from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.db.connection import Base



class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(String, nullable=True)
    precio_base = Column(Numeric(10, 2), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    categoria = relationship("Category", back_populates="productos")
    variantes = relationship("Variante", back_populates="producto", cascade="all, delete-orphan")
    resenas = relationship("Resena", back_populates="producto")


Product = Producto
