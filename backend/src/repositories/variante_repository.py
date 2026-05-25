from sqlalchemy.orm import Session

from src.db.models.product_model import Producto
from src.db.models.variante_model import Variante
from src.mappers.variante_mapper import map_variante


class VarianteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_sku(self, sku: str) -> Variante | None:
        return self.db.query(Variante).filter(Variante.sku == sku).first()

    def create_variant(self, data):
        variante = Variante(
            producto_id=data.producto_id,
            talle=data.talle,
            color=data.color,
            stock=data.stock,
            sku=data.sku,
        )
        self.db.add(variante)
        self.db.commit()
        self.db.refresh(variante)
        return map_variante(variante)

    def list_variants_by_product(self, producto_id: int):
        variantes = (
            self.db.query(Variante)
            .filter(Variante.producto_id == producto_id)
            .order_by(Variante.id.asc())
            .all()
        )
        return [map_variante(variante) for variante in variantes]

    def update_stock(self, variante_id: int, stock: int):
        variante = self.db.query(Variante).filter(Variante.id == variante_id).first()
        if not variante:
            return None

        variante.stock = stock
        self.db.commit()
        self.db.refresh(variante)
        return map_variante(variante)

    def get_low_stock_variants(self, umbral: int = 5) -> list[dict]:
        rows = (
            self.db.query(Variante, Producto)
            .join(Producto, Variante.producto_id == Producto.id)
            .filter(Variante.stock <= umbral)
            .order_by(Variante.stock.asc())
            .all()
        )

        return [
            {
                "id": variante.id,
                "producto_id": variante.producto_id,
                "talle": variante.talle,
                "color": variante.color,
                "stock": variante.stock,
                "sku": variante.sku,
                "producto_nombre": producto.nombre,
            }
            for variante, producto in rows
        ]
