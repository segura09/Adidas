from sqlalchemy.orm import Session
from sqlalchemy import func  # <-- ¡NUEVA IMPORTACIÓN HU14! Necesaria para sum y count

from src.db.models.compra_model import Compra
from src.db.models.compra_items_model import CompraItem
from src.db.models.variant_model import Variante
from src.db.models.cupon_model import Cupon 
from src.db.models.producto_model import Producto    # <-- ¡NUEVA IMPORTACIÓN HU14!
from src.db.models.category_model import Categoria    # <-- ¡NUEVA IMPORTACIÓN HU14!


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

    # --- NUEVOS MÉTODOS HU14 (REPORTE DE FACTURACIÓN) ---

    def get_billing_summary(self, desde, hasta):
        """Calcula el total bruto facturado y la cantidad de compras exitosas (HU7)."""
        estados_validos = ["pagada", "enviada", "entregada"]
        
        resultado = self.db.query(
            func.sum(Compra.total).label("total_facturado"),
            func.count(Compra.id).label("cantidad_compras")
        ).filter(
            Compra.fecha >= desde,
            Compra.fecha <= hasta,
            Compra.estado.in_(estados_validos)
        ).first()

        return {
            "total_facturado": float(resultado.total_facturado or 0.0),
            "cantidad_compras": resultado.cantidad_compras or 0
        }

    def get_billing_by_category(self, desde, hasta):
        """Calcula la facturación total desglosada y agrupada por cada categoría (HU1)."""
        estados_validos = ["pagada", "enviada", "entregada"]

        resultados = self.db.query(
            Categoria.nombre.label("categoria"),
            func.sum(CompraItem.cantidad * CompraItem.precio_unitario).label("total_categoria")
        ).join(Variante, CompraItem.variante_id == Variante.id)\
         .join(Producto, Variante.producto_id == Producto.id)\
         .join(Categoria, Producto.categoria_id == Categoria.id)\
         .join(Compra, CompraItem.compra_id == Compra.id)\
         .filter(
            Compra.fecha >= desde,
            Compra.fecha <= hasta,
            Compra.estado.in_(estados_validos)
         ).group_by(Categoria.nombre).all()

        return [{"categoria": r.categoria, "total": float(r.total_categoria or 0.0)} for r in resultados]