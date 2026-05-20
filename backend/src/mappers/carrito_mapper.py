from src.dtos.carrito_dto import CartResponseDTO, CartItemResponseDTO

def map_to_cart_response(cliente_id: int, db_rows: list) -> CartResponseDTO:
    items_dto = []
    total_carrito = 0.0

    for row in db_rows:
        # Validación robusta por si tu base de datos retorna diccionarios o tuplas
        is_dict = isinstance(row, dict)
        
        variante_id = row["variante_id"] if is_dict else row[0]
        producto_nombre = row["producto_nombre"] if is_dict else row[1]
        talle = row["talle"] if is_dict else row[2]
        precio_base = float(row["precio_base"]) if is_dict else float(row[3])
        cantidad = int(row["cantidad"]) if is_dict else int(row[4])
        color = row["color"] if is_dict else row[5]
        
        subtotal = cantidad * precio_base
        total_carrito += subtotal

        items_dto.append(
            CartItemResponseDTO(
                variante_id=variante_id,
                producto_nombre=producto_nombre,
                talle=talle,
                color=color,
                precio_unitario=precio_base,
                cantidad=cantidad,
                subtotal=subtotal
            )
        )

    return CartResponseDTO(
        cliente_id=cliente_id,
        items=items_dto,
        total=total_carrito
    )