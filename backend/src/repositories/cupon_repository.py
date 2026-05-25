from sqlalchemy.orm import Session

from src.db.models.cupon_model import Cupon


class CuponRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, codigo: str, porcentaje_descuento: float, fecha_vencimiento, usos_maximos: int) -> Cupon:
        cupon = Cupon(
            codigo=codigo,
            porcentaje_descuento=porcentaje_descuento,
            fecha_vencimiento=fecha_vencimiento,
            usos_maximos=usos_maximos,
            usos_actuales=0,
        )
        self.db.add(cupon)
        self.db.commit()
        self.db.refresh(cupon)
        return cupon

    def find_by_codigo(self, codigo: str) -> Cupon | None:
        return self.db.query(Cupon).filter(Cupon.codigo == codigo).first()

    def list_all(self) -> list[Cupon]:
        return self.db.query(Cupon).order_by(Cupon.id.desc()).all()

    def increment_usage(self, cupon: Cupon) -> Cupon:
        cupon.usos_actuales += 1
        self.db.commit()
        self.db.refresh(cupon)
        return cupon
