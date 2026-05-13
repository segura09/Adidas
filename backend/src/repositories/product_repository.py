from sqlalchemy.orm import Session

from src.db.models.product_model import Product
from src.db.models.variant_model import Variant


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        nombre: str,
        descripcion: str,
        precio_base: float,
        categoria_id: int,
        activo: bool,
    ) -> Product:
        product = Product(
            nombre=nombre,
            descripcion=descripcion,
            precio_base=precio_base,
            categoria_id=categoria_id,
            activo=activo,
        )

        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)

        return product

    def find_by_id(self, product_id: int) -> Product | None:
        return (
            self.db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

    def list_all(self) -> list[Product]:
        return (
            self.db.query(Product)
            .join(Variant)
            .filter(
                Product.activo == True,
                Variant.stock > 0,
            )
            .distinct()
            .all()
        )

    def search_products(
        self,
        categoria: int | None = None,
        talle: str | None = None,
        color: str | None = None,
    ):
        query = (
            self.db.query(Product)
            .join(Variant)
            .filter(
                Product.activo == True,
                Variant.stock > 0,
            )
        )

        if categoria:
            query = query.filter(Product.categoria_id == categoria)

        if talle:
            query = query.filter(Variant.talle == talle)

        if color:
            query = query.filter(Variant.color == color)

        return query.distinct().all()

    def update(self, product_id: int, **fields) -> Product | None:
        product = self.find_by_id(product_id)

        if product:
            for key, value in fields.items():
                if value is not None:
                    setattr(product, key, value)

            self.db.commit()
            self.db.refresh(product)

        return product

    def delete(self, product_id: int) -> bool:
        product = self.find_by_id(product_id)

        if product:
            self.db.delete(product)
            self.db.commit()
            return True

        return False