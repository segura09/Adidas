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