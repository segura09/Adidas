from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.db.connection import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(150), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    direccion = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    compras = relationship("Compra", back_populates="cliente")