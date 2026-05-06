from sqlalchemy import Column, Integer, String, Numeric, DateTime, Date
from sqlalchemy.sql import func

class Cupon(Base):
    __tablename__ = "cupones"

    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), unique=True, nullable=False)
    porcentaje_descuento = Column(Numeric(5, 2), nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    usos_maximos = Column(Integer, default=1)
    usos_actuales = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())