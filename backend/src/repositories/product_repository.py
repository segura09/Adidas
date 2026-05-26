from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from src.db.models.compra_items_model import CompraItem
from src.db.models.compra_model import Compra
from src.db.models.product_model import Producto
from src.db.models.variante_model import Variante


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        nombre: str,
        descripcion: str | None,
        precio_base: float,
        categoria_id: int,
        activo: bool = True,
    ) -> Producto:
        product = Producto(
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

    def find_by_id(self, product_id: int) -> Producto | None:
        return self.db.query(Producto).filter(Producto.id == product_id).first()

    def list_all(self) -> list[Producto]:
        return self.db.query(Producto).filter(Producto.activo == True).all()

    def search_products(
        self,
        categoria: int | None = None,
        talle: str | None = None,
        color: str | None = None,
    ) -> list[Producto]:
        query = self.db.query(Producto).filter(Producto.activo == True)

        if talle or color:
            query = query.join(Variante).filter(Variante.stock > 0)

        if categoria:
            query = query.filter(Producto.categoria_id == categoria)

        if talle:
            query = query.filter(func.lower(Variante.talle) == talle.strip().lower())

        if color:
            query = query.filter(func.lower(Variante.color) == color.strip().lower())

        return query.distinct().all()

    def update(self, product_id: int, **fields) -> Producto | None:
        product = self.find_by_id(product_id)
        if not product:
            return None

        for key, value in fields.items():
            if value is not None:
                setattr(product, key, value)

        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product_id: int) -> bool:
        product = self.find_by_id(product_id)
        if not product:
            return False

        product.activo = False
        self.db.commit()
        return True

    def get_top_selling_products(self, limit: int = 10) -> list[dict]:
        valid_statuses = ["pagada", "enviada", "entregada"]

        rows = (
            self.db.query(
                Producto.id,
                Producto.nombre,
                Producto.precio_base,
                func.sum(CompraItem.cantidad).label("unidades_vendidas"),
                func.sum(CompraItem.cantidad * CompraItem.precio_unitario).label("facturacion_acumulada"),
            )
            .join(Variante, Variante.producto_id == Producto.id)
            .join(CompraItem, CompraItem.variante_id == Variante.id)
            .join(Compra, CompraItem.compra_id == Compra.id)
            .filter(Compra.estado.in_(valid_statuses))
            .group_by(Producto.id, Producto.nombre, Producto.precio_base)
            .order_by(desc(func.sum(CompraItem.cantidad)))
            .limit(limit)
            .all()
        )

        return [
            {
                "producto_id": row.id,
                "nombre": row.nombre,
                "precio": float(row.precio_base or 0),
                "unidades_vendidas": int(row.unidades_vendidas or 0),
                "facturacion": float(row.facturacion_acumulada or 0),
            }
            for row in rows
        ]
