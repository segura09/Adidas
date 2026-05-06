from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.db.connection import Base


class CompraItem(Base):
    __tablename__ = "compra_items"

    compra_id = Column(Integer, ForeignKey("compras.id", ondelete="CASCADE"), primary_key=True)
    variante_id = Column(Integer, ForeignKey("variantes.id"), primary_key=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    compra = relationship("Compra", back_populates="items")
    variante = relationship("Variante")