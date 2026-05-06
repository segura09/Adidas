from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.db.connection import Base

class Variante(Base):
    __tablename__ = "variantes"

    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey("productos.id", ondelete="CASCADE"), nullable=False)
    talle = Column(String(20), nullable=False)
    color = Column(String(50), nullable=False)
    stock = Column(Integer, default=0)
    sku = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    producto = relationship("Producto", back_populates="variantes")