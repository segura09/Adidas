# backend/src/db/models/resena_model.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from src.db.base import Base  # O la ruta de tu Base declarativa

class Resena(Base):
    __tablename__ = "resenas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    calificacion = Column(Integer, nullable=False)  # Check constraint de 1 a 5 se maneja en DB/Schema
    comentario = Column(String, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relaciones alternativas
    producto = relationship("Producto", back_populates="resenas")
    # cliente = relationship("Usuario")

    __table_args__ = (
        UniqueConstraint("cliente_id", "producto_id", name="uq_cliente_producto_resena"),
    )