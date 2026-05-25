def devolucion_to_response(devolucion):
    return {
        "id": devolucion.id,
        "compra_id": devolucion.compra_id,
        "estado": devolucion.estado,
        "motivo": devolucion.motivo,
        "items": [
            {"variante_id": item.variante_id, "cantidad": item.cantidad}
            for item in devolucion.items
        ],
    }
