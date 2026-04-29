from src.db.models.category_model import Category
from src.dtos.category_dto import CategoryResponseDTO


def to_category_response(category: Category) -> CategoryResponseDTO:
    """Convierte un Model SQLAlchemy en un DTO de respuesta (sin campos sensibles)."""
    return CategoryResponseDTO.model_validate(category)