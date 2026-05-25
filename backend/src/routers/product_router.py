from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.db.connection import get_db
from src.dtos.product_dto import CreateProductDTO, ProductResponseDTO, UpdateProductDTO
from src.schemas.product_schema import CreateProductSchema, UpdateProductSchema
from src.services.product_service import ProductService
from src.repositories.variante_repository import VarianteRepository
from src.schemas.variante_schema import VarianteCreate, VarianteResponse
from src.services.variante_service import VarianteService


router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/top")
def get_top_products(
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    return ProductService(db).get_top_selling_products(limit=limit)


@router.get("", response_model=list[ProductResponseDTO])
@router.get("/", response_model=list[ProductResponseDTO])
def list_products(db: Session = Depends(get_db)):
    return ProductService(db).list_all()


@router.post("", response_model=ProductResponseDTO, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=ProductResponseDTO, status_code=status.HTTP_201_CREATED)
def create_product(payload: CreateProductSchema, db: Session = Depends(get_db)):
    dto = CreateProductDTO(**payload.model_dump())
    return ProductService(db).create(dto)


@router.get("/buscar", response_model=list[ProductResponseDTO])
@router.get("/search", response_model=list[ProductResponseDTO])
def search_products(
    categoria: int | None = Query(default=None),
    talle: str | None = Query(default=None),
    color: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return ProductService(db).search_products(
        categoria=categoria,
        talle=talle,
        color=color,
    )


@router.get("/{product_id}", response_model=ProductResponseDTO)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return ProductService(db).get_by_id(product_id)


@router.get("/{product_id}/variantes", response_model=list[VarianteResponse])
def list_product_variants(product_id: int, db: Session = Depends(get_db)):
    return VarianteService(VarianteRepository(db)).list_variants_by_product(product_id)


@router.post("/{product_id}/variantes", response_model=VarianteResponse, status_code=status.HTTP_201_CREATED)
def create_product_variant(product_id: int, payload: VarianteCreate, db: Session = Depends(get_db)):
    data = payload.model_copy(update={"producto_id": product_id})
    return VarianteService(VarianteRepository(db)).create_variant(data)


@router.put("/{product_id}", response_model=ProductResponseDTO)
def update_product(
    product_id: int,
    payload: UpdateProductSchema,
    db: Session = Depends(get_db),
):
    dto = UpdateProductDTO(**payload.model_dump(exclude_unset=True))
    return ProductService(db).update(product_id, dto)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    ProductService(db).delete(product_id)
    return
