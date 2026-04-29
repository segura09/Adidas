from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.db.connection import get_db
from src.dtos.category_dto import CreateCategoryDTO, CategoryResponseDTO
from src.schemas.category_schema import CreateCategorySchema
from src.services.category_services import CategoryService

router = APIRouter(prefix="/category", tags=["category"])


@router.post("/", response_model=CategoryResponseDTO, status_code=status.HTTP_201_CREATED)
def create_category(payload: CreateCategorySchema, db: Session = Depends(get_db)):
    """Ejemplo completo: valida con Schema, arma DTO, llama al service."""
    dto = CreateCategoryDTO(**payload.model_dump())
    return CategoryService(db).create(dto)
