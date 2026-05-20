from src.mappers.variante_mapper import map_variante


class VarianteRepository:

    def __init__(self, db):
        self.db = db

    def get_by_sku(self, sku):
        query = "SELECT * FROM variantes WHERE sku = %s"
        result = self.db.fetch_one(query, (sku,))
        return result

    def create_variant(self, data):
        query = """
        INSERT INTO variantes
        (producto_id, talle, color, stock, sku)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *
        """

        result = self.db.fetch_one(
            query,
            (
                data.producto_id,
                data.talle,
                data.color,
                data.stock,
                data.sku
            )
        )

        return map_variante(result)

    def list_variants_by_product(self, producto_id):
        query = "SELECT * FROM variantes WHERE producto_id = %s"

        results = self.db.fetch_all(query, (producto_id,))

        return [map_variante(row) for row in results]

    def update_stock(self, variante_id, stock):
        query = """
        UPDATE variantes
        SET stock = %s
        WHERE id = %s
        RETURNING *
        """

        result = self.db.fetch_one(query, (stock, variante_id))

        return map_variante(result)

    # =========================================================================
    # NUEVO MÉTODO: HU10 — Stock bajo
    # =========================================================================
    def get_low_stock_variants(self, umbral: int = 5) -> list[dict]:
        """
        Obtiene las variantes con stock menor o igual al umbral, 
        haciendo un JOIN con la tabla de productos para traer su contexto (nombre).
        """
        query = """
            SELECT 
                v.id AS variante_id,
                v.talle,
                v.color,
                v.stock,
                v.sku,
                p.id AS producto_id,
                p.nombre AS producto_nombre
            FROM variantes v
            INNER JOIN productos p ON v.producto_id = p.id
            WHERE v.stock <= %s
            ORDER BY v.stock ASC
        """
        
        # Usamos fetch_all porque esperamos una lista de filas resultantes
        results = self.db.fetch_all(query, (umbral,))
        
        # Al ser un resultado mixto (Variante + Producto), lo mapeamos a diccionarios
        # estructurados para que el JSON final quede limpio y entendible.
        return [
            {
                "id": row["variante_id"] if isinstance(row, dict) else row[0],
                "talle": row["talle"] if isinstance(row, dict) else row[1],
                "color": row["color"] if isinstance(row, dict) else row[2],
                "stock": row["stock"] if isinstance(row, dict) else row[3],
                "sku": row["sku"] if isinstance(row, dict) else row[4],
                "producto": {
                    "id": row["producto_id"] if isinstance(row, dict) else row[5],
                    "nombre": row["producto_nombre"] if isinstance(row, dict) else row[6]
                }
            }
            for row in results
        ]