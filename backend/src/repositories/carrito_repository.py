class CarritoRepository:
    def __init__(self, db):
        self.db = db

    def ensure_cart_exists(self, cliente_id: int) -> None:
        """Verifica si el cliente tiene un carrito; si no, lo inicializa."""
        query_find = "SELECT cliente_id FROM carritos WHERE cliente_id = %s"
        cart = self.db.fetch_one(query_find, (cliente_id,))
        
        if not cart:
            query_create = "INSERT INTO carritos (cliente_id) VALUES (%s)"
            self.db.fetch_one(query_create, (cliente_id,))

    def get_variant_stock_and_price(self, variante_id: int):
        """Retorna el stock de la variante y el precio base del producto asociado."""
        query = """
            SELECT v.stock, p.precio_base 
            FROM variantes v
            INNER JOIN productos p ON v.producto_id = p.id
            WHERE v.id = %s
        """
        return self.db.fetch_one(query, (variante_id,))

    def add_or_update_item(self, cliente_id: int, variante_id: int, cantidad: int):
        """Inserta el ítem en el carrito o incrementa de forma acumulativa si ya existe."""
        query = """
            INSERT INTO carrito_items (cliente_id, variante_id, cantidad)
            VALUES (%s, %s, %s)
            ON CONFLICT (cliente_id, variante_id)
            DO UPDATE SET cantidad = carrito_items.cantidad + EXCLUDED.cantidad
            RETURNING *
        """
        return self.db.fetch_one(query, (cliente_id, variante_id, cantidad))

    def get_cart_details(self, cliente_id: int) -> list:
        """Recupera los ítems del carrito con todo su contexto (Producto, Talle, Color, Precio)."""
        query = """
            SELECT 
                ci.variante_id,
                p.nombre AS producto_nombre,
                v.talle,
                p.precio_base,
                ci.cantidad,
                v.color
            FROM carrito_items ci
            INNER JOIN variantes v ON ci.variante_id = v.id
            INNER JOIN productos p ON v.producto_id = p.id
            WHERE ci.cliente_id = %s
        """
        return self.db.fetch_all(query, (cliente_id,))

    def clear_cart(self, cliente_id: int) -> None:
        """Elimina todos los ítems asociados al carrito del cliente."""
        query = "DELETE FROM carrito_items WHERE cliente_id = %s"
        self.db.fetch_one(query, (cliente_id,))

    def create_order_from_cart(self, cliente_id: int, total_carrito: float) -> int:
        """Mueve transaccionalmente el carrito a una compra y descuenta stock."""
        # 1. Crear el registro maestro de la Compra (estado por defecto: 'pendiente_pago')
        query_compra = """
            INSERT INTO compras (cliente_id, total, estado)
            VALUES (%s, %s, 'pendiente_pago')
            RETURNING id
        """
        compra = self.db.fetch_one(query_compra, (cliente_id, total_carrito))
        compra_id = compra["id"] if isinstance(compra, dict) else compra[0]

        # 2. Trasladar los detalles del carrito directo a compra_items
        query_move_items = """
            INSERT INTO compra_items (compra_id, variante_id, cantidad, precio_unitario)
            SELECT %s, ci.variante_id, ci.cantidad, p.precio_base
            FROM carrito_items ci
            INNER JOIN variantes v ON ci.variante_id = v.id
            INNER JOIN productos p ON v.producto_id = p.id
            WHERE ci.cliente_id = %s
        """
        self.db.fetch_one(query_move_items, (compra_id, cliente_id))

        # 3. Descontar las unidades compradas del stock de variantes
        query_update_stock = """
            UPDATE variantes v
            SET stock = v.stock - ci.cantidad
            FROM carrito_items ci
            WHERE v.id = ci.variante_id AND ci.cliente_id = %s
        """
        self.db.fetch_one(query_update_stock, (cliente_id,))

        return compra_id