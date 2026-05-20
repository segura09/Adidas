from src.db.models.product_model import Producto
from src.dtos.product_dto import ProductResponseDTO


def to_product_response(product: Producto) -> ProductResponseDTO:
    return ProductResponseDTO.model_validate(product)
