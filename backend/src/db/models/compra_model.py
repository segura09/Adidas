from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.db.connection import Base
class Compra(Base):
    __tablename__ = "compras"

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    fecha = Column(DateTime, server_default=func.now()) # Este cumple el rol de 'fecha' de la HU
    total = Column(Numeric(10, 2), nullable=False)
    estado = Column(String(50), default="pendiente_pago")
    cupon_id = Column(Integer, ForeignKey("cupones.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    cliente = relationship("Cliente", back_populates="compras")
    items = relationship("CompraItem", back_populates="compra")