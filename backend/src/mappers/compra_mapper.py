def compra_to_response(compra):
    return {
        "id": compra.id,
        "cliente_id": compra.cliente_id,
        "fecha": compra.fecha or compra.created_at,
        "total": float(compra.total),
        "estado": compra.estado,
        "cupon_codigo": getattr(getattr(compra, "cupon", None), "codigo", None),
        "items": [
            {
                "variante_id": item.variante_id,
                "cantidad": item.cantidad,
                "precio_unitario": float(item.precio_unitario),
                "subtotal": float(item.precio_unitario) * item.cantidad,
            }
            for item in compra.items
        ]
    }
