from sqlalchemy.orm import Session

from src.dtos.category_dto import CreateCategoryDTO, CategoryResponseDTO
from src.mappers.category_mapper import to_category_response
from src.repositories.category_repository import CategoryRepository
class CategoryService:
    def __init__(self, db: Session):
        self.repo = CategoryRepository(db)

    def create(self, dto: CreateCategoryDTO) -> CategoryResponseDTO:
        category = self.repo.create(
            nombre=dto.nombre,
            descripcion=dto.descripcion
        )
        return to_category_response(category)

    def list_all(self) -> list[CategoryResponseDTO]:
        return [to_category_response(category) for category in self.repo.find_all()]

