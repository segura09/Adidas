from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.db.connection import Base


class Carrito(Base):
    __tablename__ = "carritos"

    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"), primary_key=True)
    fecha_creacion = Column(DateTime, server_default=func.now())

    items = relationship("CarritoItem", back_populates="carrito", cascade="all, delete-orphan")


class CarritoItem(Base):
    __tablename__ = "carrito_items"

    cliente_id = Column(
        Integer,
        ForeignKey("carritos.cliente_id", ondelete="CASCADE"),
        primary_key=True,
    )
    variante_id = Column(Integer, ForeignKey("variantes.id"), primary_key=True)
    cantidad = Column(Integer, nullable=False)

    carrito = relationship("Carrito", back_populates="items")
    variante = relationship("Variante")
