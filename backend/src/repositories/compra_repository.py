from sqlalchemy import func
from sqlalchemy.orm import Session

from src.db.models.category_model import Category
from src.db.models.compra_items_model import CompraItem
from src.db.models.compra_model import Compra
from src.db.models.cupon_model import Cupon
from src.db.models.product_model import Producto
from src.db.models.variante_model import Variante


class CompraRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_variant_by_id(self, variante_id: int):
        return self.db.query(Variante).filter(Variante.id == variante_id).first()

    def create_purchase(
        self,
        usuario_id: int,
        total: float,
        cupon_id: int = None,
        estado: str = "pendiente_pago",
    ):
        compra = Compra(
            cliente_id=usuario_id,
            total=total,
            cupon_id=cupon_id,
            estado=estado,
        )

        self.db.add(compra)
        self.db.flush()

        return compra

    def save_purchase_items(self, compra_id: int, items: list):
        for item in items:
            compra_item = CompraItem(
                compra_id=compra_id,
                variante_id=item["variante_id"],
                cantidad=item["cantidad"],
                precio_unitario=item["precio_unitario"],
            )
            self.db.add(compra_item)

    def reserve_stock(self, variant: Variante, cantidad: int):
        variant.stock -= cantidad

    def get_coupon_by_code(self, codigo: str):
        return self.db.query(Cupon).filter(Cupon.codigo == codigo).first()

    def increment_coupon_use(self, cupon: Cupon):
        cupon.usos_actuales += 1

    def get_billing_summary(self, desde, hasta):
        estados_validos = ["pagada", "enviada", "entregada"]

        resultado = self.db.query(
            func.sum(Compra.total).label("total_facturado"),
            func.count(Compra.id).label("cantidad_compras"),
        ).filter(
            Compra.fecha >= desde,
            Compra.fecha <= hasta,
            Compra.estado.in_(estados_validos),
        ).first()

        return {
            "total_facturado": float(resultado.total_facturado or 0.0),
            "cantidad_compras": resultado.cantidad_compras or 0,
        }

    def get_billing_by_category(self, desde, hasta):
        estados_validos = ["pagada", "enviada", "entregada"]

        resultados = self.db.query(
            Category.nombre.label("categoria"),
            func.sum(CompraItem.cantidad * CompraItem.precio_unitario).label("total_categoria"),
        ).join(Variante, CompraItem.variante_id == Variante.id)\
         .join(Producto, Variante.producto_id == Producto.id)\
         .join(Category, Producto.categoria_id == Category.id)\
         .join(Compra, CompraItem.compra_id == Compra.id)\
         .filter(
            Compra.fecha >= desde,
            Compra.fecha <= hasta,
            Compra.estado.in_(estados_validos),
         ).group_by(Category.nombre).all()

        return [
            {"categoria": r.categoria, "total": float(r.total_categoria or 0.0)}
            for r in resultados
        ]

    def get_by_id(self, compra_id: int) -> Compra | None:
        return self.db.query(Compra).filter(Compra.id == compra_id).first()

    def list_all(self, estado: str | None = None) -> list[Compra]:
        query = self.db.query(Compra).order_by(Compra.fecha.desc(), Compra.id.desc())
        if estado:
            query = query.filter(Compra.estado == estado)
        else:
            query = query.filter(Compra.estado != "cancelada")
        return query.all()

    def update_estado(self, compra_id: int, estado: str) -> Compra | None:
        compra = self.get_by_id(compra_id)
        if not compra:
            return None

        compra.estado = estado
        self.db.commit()
        self.db.refresh(compra)
        return compra
