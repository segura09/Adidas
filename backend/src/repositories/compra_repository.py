from sqlalchemy.orm import Session

from src.db.models.compra_model import Compra
from src.db.models.compra_items_model import CompraItem
from src.db.models.variant_model import Variante
from src.db.models.cupon_model import Cupon  # <-- ¡NUEVA IMPORTACIÓN HU6!


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
        total: float,
        cupon_id: int = None  
    ):
        compra = Compra(
            usuario_id=usuario_id, 
            total=total,
            cupon_id=cupon_id 
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


    def get_coupon_by_code(self, codigo: str):
        """Busca un cupón activo en la base de datos por su código string."""
        return self.db.query(Cupon).filter(Cupon.codigo == codigo).first()

    def increment_coupon_use(self, cupon: Cupon):
        """Incrementa el contador de usos del cupón en la sesión actual."""
        cupon.usos_actuales += 1