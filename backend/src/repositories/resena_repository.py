from sqlalchemy import func
from sqlalchemy.orm import Session

from src.db.models.compra_items_model import CompraItem
from src.db.models.compra_model import Compra
from src.db.models.resena_model import Resena


class ResenaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> Resena:
        resena = Resena(**data)
        self.db.add(resena)
        return resena

    def find_by_id(self, resena_id: int) -> Resena | None:
        return self.db.query(Resena).filter(Resena.id == resena_id).first()

    def get_by_cliente_and_producto(self, cliente_id: int, producto_id: int) -> Resena | None:
        return self.db.query(Resena).filter(
            Resena.cliente_id == cliente_id,
            Resena.producto_id == producto_id,
        ).first()

    def has_delivered_purchase(self, cliente_id: int, producto_id: int) -> bool:
        return self.db.query(Compra).join(CompraItem).filter(
            Compra.cliente_id == cliente_id,
            Compra.estado == "entregada",
            CompraItem.variante.has(producto_id=producto_id),
        ).first() is not None

    def list_by_producto(self, producto_id: int) -> list[Resena]:
        return self.db.query(Resena).filter(Resena.producto_id == producto_id).all()

    def get_summary_by_producto(self, producto_id: int) -> dict:
        total_resenas, promedio = self.db.query(
            func.count(Resena.id),
            func.coalesce(func.avg(Resena.calificacion), 0),
        ).filter(Resena.producto_id == producto_id).one()

        return {
            "producto_id": producto_id,
            "promedio_calificaciones": float(promedio),
            "total_resenas": total_resenas,
        }

    def list_all(self) -> list[Resena]:
        return self.db.query(Resena).all()

    def update(self, resena_id: int, **fields) -> Resena | None:
        resena = self.find_by_id(resena_id)
        if not resena:
            return None

        for key, value in fields.items():
            if hasattr(resena, key):
                setattr(resena, key, value)

        self.db.commit()
        self.db.refresh(resena)
        return resena

    def delete(self, resena_id: int) -> bool:
        resena = self.find_by_id(resena_id)
        if not resena:
            return False

        self.db.delete(resena)
        self.db.commit()
        return True
