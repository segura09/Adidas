from sqlalchemy import Column, Date, Integer, Numeric, String
from src.db.connection import Base

class Cupon(Base):
    __tablename__ = "cupones"

    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), unique=True, nullable=False)
    porcentaje_descuento = Column(Numeric(5, 2), nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    usos_maximos = Column(Integer, default=1)
    usos_actuales = Column(Integer, default=0)
