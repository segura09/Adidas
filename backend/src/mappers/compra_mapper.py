def compra_to_response(compra):

    return {
        "id": compra.id,
        "usuario_id": compra.usuario_id,
        "total": float(compra.total),
        "created_at": compra.created_at,
        "items": [
            {
                "variante_id": item.variante_id,
                "cantidad": item.cantidad,
                "precio_unitario": float(item.precio_unitario),
                "subtotal": float(item.subtotal)
            }
            for item in compra.items
        ]
    }