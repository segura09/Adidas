def compra_to_response(compra):
    subtotal = sum(float(item.precio_unitario) * item.cantidad for item in compra.items)
    total = float(compra.total)
    descuento = max(subtotal - total, 0.0)

    return {
        "id": compra.id,
        "cliente_id": compra.cliente_id,
        "fecha": compra.fecha,
        "total": total,
        "subtotal": subtotal,
        "descuento": descuento,
        "estado": compra.estado,
        "cupon_codigo": getattr(getattr(compra, "cupon", None), "codigo", None),
        "items": [
            {
                "variante_id": item.variante_id,
                "cantidad": item.cantidad,
                "precio_unitario": float(item.precio_unitario),
                "subtotal": float(item.precio_unitario) * item.cantidad,
                "producto_nombre": getattr(getattr(item.variante, "producto", None), "nombre", None),
                "talle": getattr(item.variante, "talle", None),
                "color": getattr(item.variante, "color", None),
            }
            for item in compra.items
        ]
    }
