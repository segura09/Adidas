from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

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

    def delete(self, category_id: int) -> None:
        try:
            deleted = self.repo.delete(category_id)
        except IntegrityError:
            self.repo.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar una categoria con productos asociados.",
            )

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoria no encontrada.",
            )
