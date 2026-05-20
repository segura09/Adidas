from fastapi import HTTPException
from src.repositories.carrito_repository import CarritoRepository
from src.mappers.carrito_mapper import map_to_cart_response
from src.dtos.carrito_dto import CartResponseDTO

class CarritoService:
    def __init__(self, repository: CarritoRepository):
        self.repo = repository

    def add_item_to_cart(self, cliente_id: int, variante_id: int, cantidad: int) -> CartResponseDTO:
        # 1. Validar la existencia de la variante y verificar stock
        variant_data = self.repo.get_variant_stock_and_price(variante_id)
        if not variant_data:
            raise HTTPException(status_code=404, detail="La variante especificada no existe")
        
        is_dict = isinstance(variant_data, dict)
        stock_actual = variant_data["stock"] if is_dict else variant_data[0]

        if stock_actual < cantidad:
            raise HTTPException(
                status_code=400, 
                detail=f"Stock insuficiente para añadir al carrito. Stock disponible: {stock_actual}"
            )

        # 2. Asegurar que exista el carrito y guardar el ítem
        self.repo.ensure_cart_exists(cliente_id)
        self.repo.add_or_update_item(cliente_id, variante_id, cantidad)

        # 3. Retornar el carrito estructurado actualizado
        return self.get_cart(cliente_id)

    def get_cart(self, cliente_id: int) -> CartResponseDTO:
        self.repo.ensure_cart_exists(cliente_id)
        rows = self.repo.get_cart_details(cliente_id)
        return map_to_cart_response(cliente_id, rows)

    def clear_cart(self, cliente_id: int) -> dict:
        self.repo.ensure_cart_exists(cliente_id)
        self.repo.clear_cart(cliente_id)
        return {"detail": "Carrito vaciado correctamente"}

    def checkout_from_cart(self, cliente_id: int) -> dict:
        self.repo.ensure_cart_exists(cliente_id)
        items = self.repo.get_cart_details(cliente_id)
        
        if not items:
            raise HTTPException(status_code=400, detail="No se puede realizar el checkout de un carrito vacío")

        # Doble validación de stock crítico para asegurar consistencia concurrente antes de comprar
        total_compra = 0.0
        for item in items:
            is_dict = isinstance(item, dict)
            v_id = item["variante_id"] if is_dict else item[0]
            nombre_p = item["producto_nombre"] if is_dict else item[1]
            precio_p = float(item["precio_base"]) if is_dict else float(item[3])
            cant = int(item["cantidad"]) if is_dict else int(item[4])
            
            total_compra += (cant * precio_p)

            # Re-verificar stock remanente
            v_data = self.repo.get_variant_stock_and_price(v_id)
            stock_db = v_data["stock"] if isinstance(v_data, dict) else v_data[0]
            if stock_db < cant:
                raise HTTPException(
                    status_code=400, 
                    detail=f"El producto '{nombre_p}' ya no cuenta con stock suficiente para el checkout (Disponible: {stock_db})."
                )

        # Procesar orden, vaciar carrito y retornar ID de la compra generada
        compra_id = self.repo.create_order_from_cart(cliente_id, total_compra)
        self.repo.clear_cart(cliente_id)

        return {
            "detail": "Compra registrada con éxito a partir del carrito",
            "compra_id": compra_id,
            "estado": "pendiente_pago"
        }