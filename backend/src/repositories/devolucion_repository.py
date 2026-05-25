from sqlalchemy.orm import Session

from src.db.models.compra_model import Compra
from src.db.models.devolucion_items_model import DevolucionItem
from src.db.models.devolucion_model import Devolucion
from src.db.models.variante_model import Variante


class DevolucionRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, devolucion_id: int) -> Devolucion | None:
        return self.db.query(Devolucion).filter(Devolucion.id == devolucion_id).first()

    def find_compra_by_id(self, compra_id: int) -> Compra | None:
        return self.db.query(Compra).filter(Compra.id == compra_id).first()

    def create_devolucion(self, compra_id: int, items: list[dict], motivo: str | None = None) -> Devolucion:
        devolucion = Devolucion(compra_id=compra_id, estado="solicitada", motivo=motivo)
        self.db.add(devolucion)
        self.db.flush()

        for item in items:
            self.db.add(
                DevolucionItem(
                    devolucion_id=devolucion.id,
                    variante_id=item["variante_id"],
                    cantidad=item["cantidad"],
                    motivo=item.get("motivo", motivo),
                )
            )

        self.db.commit()
        self.db.refresh(devolucion)
        return devolucion

    def update_estado(self, devolucion: Devolucion, nuevo_estado: str) -> Devolucion:
        devolucion.estado = nuevo_estado
        self.db.commit()
        self.db.refresh(devolucion)
        return devolucion

    def increment_variant_stock(self, variante_id: int, cantidad: int):
        variante = self.db.query(Variante).filter(Variante.id == variante_id).first()
        if variante:
            variante.stock += cantidad
            self.db.commit()
