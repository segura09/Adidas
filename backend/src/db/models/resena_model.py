# backend/src/db/models/resena_model.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from src.db.connection import Base  

class Resena(Base):
    __tablename__ = "resenas"

    id = Column(Integer, primary_key=True, index=True)
    
    
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False) 
    
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    calificacion = Column(Integer, nullable=False)  
    comentario = Column(String, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    producto = relationship("Producto", back_populates="resenas")
    # cliente = relationship("Usuario")

    __table_args__ = (
        UniqueConstraint("usuario_id", "producto_id", name="uq_usuario_producto_resena"),
    )