from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.db.connection import Base


class DevolucionItem(Base):
    __tablename__ = "devolucion_items"

    id = Column(Integer, primary_key=True)
    devolucion_id = Column(Integer, ForeignKey("devoluciones.id", ondelete="CASCADE"), nullable=False)
    variante_id = Column(Integer, ForeignKey("variantes.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    motivo = Column(String, nullable=True)

    devolucion = relationship("Devolucion", back_populates="items")
