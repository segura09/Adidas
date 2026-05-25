from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.connection import get_db
from src.dtos.category_dto import CreateCategoryDTO, CategoryResponseDTO
from src.schemas.category_schema import CreateCategorySchema
from src.services.category_services import CategoryService

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.get("", response_model=list[CategoryResponseDTO])
@router.get("/", response_model=list[CategoryResponseDTO])
def list_categories(db: Session = Depends(get_db)):
    return CategoryService(db).list_all()


@router.post("", response_model=CategoryResponseDTO, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=CategoryResponseDTO, status_code=status.HTTP_201_CREATED)
def create_category(payload: CreateCategorySchema, db: Session = Depends(get_db)):
    """Ejemplo completo: valida con Schema, arma DTO, llama al service."""
    dto = CreateCategoryDTO(
        nombre=payload.nombre,
        descripcion=payload.descripcion or payload.nombre,
    )
    return CategoryService(db).create(dto)
