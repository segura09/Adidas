from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from src.db.models.product_model import Product
from src.db.models.variant_model import Variant
# IMPORTANTE: Asegúrate de que las rutas a tus modelos de compra sean las correctas
from src.db.models.compra_model import Compra, CompraItem 


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
        product = self.find_id(product_id)

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

    # =========================================================================
    # NUEVO MÉTODO: HU9 — Productos más vendidos
    # =========================================================================
    def get_top_selling_products(self, limit: int = 10) -> list[dict]:
        """
        Obtiene el ranking de los productos más vendidos filtrando únicamente
        por compras que tengan un estado válido (pagada, enviada, entregada).
        Devuelve el ID, nombre, precio base, unidades vendidas y facturación acumulada.
        """
        valid_statuses = ["pagada", "enviada", "entregada"]
        
        result = (
            self.db.query(
                Product.id,
                Product.nombre,
                Product.precio_base,
                func.sum(CompraItem.cantidad).label("unidades_vendidas"),
                func.sum(CompraItem.cantidad * CompraItem.precio_unitario).label("facturacion_acumulada")
            )
            .join(CompraItem, CompraItem.producto_id == Product.id)
            .join(Compra, CompraItem.compra_id == Compra.id)
            .filter(Compra.estado.in_(valid_statuses))
            # Agrupamos por los campos seleccionados para cumplir con el estándar de SQL estricto
            .group_by(Product.id, Product.nombre, Product.precio_base)
            # Ordenamos de mayor a menor cantidad de unidades vendidas
            .order_by(desc(func.sum(CompraItem.cantidad)))
            .limit(limit)
            .all()
        )
        
        # Formateamos el resultado de forma segura validando posibles valores nulos
        return [
            {
                "id": row.id,
                "nombre": row.nombre,
                "precio": float(row.precio_base) if row.precio_base else 0.0,
                "unidades_vendidas": int(row.unidades_vendidas) if row.unidades_vendidas else 0,
                "facturacion_acumulada": float(row.facturacion_acumulada) if row.facturacion_acumulada else 0.0
            }
            for row in result
        ]