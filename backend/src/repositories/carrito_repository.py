from sqlalchemy.orm import Session

from src.db.models.carrito_model import Carrito, CarritoItem
from src.db.models.compra_items_model import CompraItem
from src.db.models.compra_model import Compra
from src.db.models.product_model import Producto
from src.db.models.variante_model import Variante


class CarritoRepository:
    def __init__(self, db: Session):
        self.db = db

    def ensure_cart_exists(self, cliente_id: int) -> None:
        cart = self.db.query(Carrito).filter(Carrito.cliente_id == cliente_id).first()
        if not cart:
            self.db.add(Carrito(cliente_id=cliente_id))
            self.db.commit()

    def get_variant_stock_and_price(self, variante_id: int):
        row = (
            self.db.query(Variante.stock, Producto.precio_base)
            .join(Producto, Variante.producto_id == Producto.id)
            .filter(Variante.id == variante_id)
            .first()
        )
        if not row:
            return None

        return {"stock": row.stock, "precio_base": row.precio_base}

    def add_or_update_item(self, cliente_id: int, variante_id: int, cantidad: int):
        item = (
            self.db.query(CarritoItem)
            .filter(
                CarritoItem.cliente_id == cliente_id,
                CarritoItem.variante_id == variante_id,
            )
            .first()
        )

        if item:
            item.cantidad += cantidad
        else:
            item = CarritoItem(
                cliente_id=cliente_id,
                variante_id=variante_id,
                cantidad=cantidad,
            )
            self.db.add(item)

        self.db.commit()
        self.db.refresh(item)
        return item

    def get_cart_details(self, cliente_id: int) -> list[dict]:
        rows = (
            self.db.query(
                CarritoItem.variante_id,
                Producto.nombre.label("producto_nombre"),
                Variante.talle,
                Producto.precio_base,
                CarritoItem.cantidad,
                Variante.color,
            )
            .join(Variante, CarritoItem.variante_id == Variante.id)
            .join(Producto, Variante.producto_id == Producto.id)
            .filter(CarritoItem.cliente_id == cliente_id)
            .all()
        )

        return [
            {
                "variante_id": row.variante_id,
                "producto_nombre": row.producto_nombre,
                "talle": row.talle,
                "precio_base": row.precio_base,
                "cantidad": row.cantidad,
                "color": row.color,
            }
            for row in rows
        ]

    def clear_cart(self, cliente_id: int) -> None:
        self.db.query(CarritoItem).filter(CarritoItem.cliente_id == cliente_id).delete()
        self.db.commit()

    def remove_item(self, cliente_id: int, variante_id: int) -> None:
        self.db.query(CarritoItem).filter(
            CarritoItem.cliente_id == cliente_id,
            CarritoItem.variante_id == variante_id,
        ).delete()
        self.db.commit()

    def create_order_from_cart(self, cliente_id: int, total_carrito: float) -> int:
        compra = Compra(
            cliente_id=cliente_id,
            total=total_carrito,
            estado="pendiente",
        )
        self.db.add(compra)
        self.db.flush()

        items = (
            self.db.query(CarritoItem, Variante, Producto)
            .join(Variante, CarritoItem.variante_id == Variante.id)
            .join(Producto, Variante.producto_id == Producto.id)
            .filter(CarritoItem.cliente_id == cliente_id)
            .all()
        )

        for cart_item, variante, producto in items:
            self.db.add(
                CompraItem(
                    compra_id=compra.id,
                    variante_id=cart_item.variante_id,
                    cantidad=cart_item.cantidad,
                    precio_unitario=producto.precio_base,
                )
            )
            variante.stock -= cart_item.cantidad

        self.db.commit()
        self.db.refresh(compra)
        return compra.id
