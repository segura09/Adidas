from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.db.connection import Base


class Devolucion(Base):
    __tablename__ = "devoluciones"

    id = Column(Integer, primary_key=True)
    compra_id = Column(Integer, ForeignKey("compras.id", ondelete="CASCADE"), nullable=False)
    estado = Column(String(30), default="solicitada", nullable=False)
    motivo = Column(String, nullable=True)
    fecha = Column(DateTime, server_default=func.now())

    compra = relationship("Compra")
    items = relationship("DevolucionItem", back_populates="devolucion", cascade="all, delete-orphan")
