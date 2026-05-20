from sqlalchemy.orm import Session

from src.db.models.compra_model import Compra
from src.db.models.compra_items_model import CompraItem
from src.db.models.variant_model import Variante


class CompraRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_variant_by_id(
        self,
        variante_id: int
    ):

        return self.db.query(Variante).filter(
            Variante.id == variante_id
        ).first()

    def create_purchase(
        self,
        usuario_id: int,
        total: float
    ):

        compra = Compra(
            usuario_id=usuario_id,
            total=total
        )

        self.db.add(compra)

        self.db.flush()

        return compra

    def save_purchase_items(
        self,
        compra_id: int,
        items: list
    ):

        for item in items:

            compra_item = CompraItem(
                compra_id=compra_id,
                variante_id=item["variante_id"],
                cantidad=item["cantidad"],
                precio_unitario=item["precio_unitario"],
                subtotal=item["subtotal"]
            )

            self.db.add(compra_item)

    def reserve_stock(
        self,
        variant: Variante,
        cantidad: int
    ):

        variant.stock -= cantidad