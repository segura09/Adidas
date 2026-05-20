from fastapi import HTTPException


class VarianteService:

    def __init__(self, repository):
        self.repository = repository

    def create_variant(self, data):

        existing_sku = self.repository.get_by_sku(data.sku)

        if existing_sku:
            raise HTTPException(
                status_code=400,
                detail="El SKU ya existe"
            )

        return self.repository.create_variant(data)

    def list_variants_by_product(self, producto_id):
        return self.repository.list_variants_by_product(producto_id)

    def update_stock(self, variante_id, stock):

        if stock < 0:
            raise HTTPException(
                status_code=400,
                detail="El stock no puede ser negativo"
            )

        return self.repository.update_stock(variante_id, stock)

    # =========================================================================
    # AGREGADO: HU10 — Stock bajo
    # =========================================================================
    def get_low_stock_variants(self, umbral: int = 5):
        """
        Llama al repositorio para obtener las variantes con stock crítico.
        Aquí podrías añadir más lógica de negocio a futuro si fuera necesario.
        """
        return self.repository.get_low_stock_variants(umbral=umbral)