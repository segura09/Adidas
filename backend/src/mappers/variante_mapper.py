from src.dtos.variante_dto import VarianteDTO


def map_variante(row):
    return VarianteDTO(
        id=row["id"],
        producto_id=row["producto_id"],
        talle=row["talle"],
        color=row["color"],
        stock=row["stock"],
        sku=row["sku"]
    )