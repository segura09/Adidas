from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from src.db.connection import get_db
from src.dtos.product_dto import CreateProductDTO, ProductResponseDTO, UpdateProductDTO
from src.schemas.product_schema import CreateProductSchema, UpdateProductSchema
from src.services.product_service import ProductService
from src.repositories.variante_repository import VarianteRepository
from src.schemas.variante_schema import VarianteCreate, VarianteResponse
from src.services.variante_service import VarianteService


router = APIRouter(prefix="/productos", tags=["Productos"])

UPLOADS_DIR = Path(__file__).resolve().parents[2] / "uploads" / "products"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


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


@router.post("/{product_id}/imagen", response_model=ProductResponseDTO)
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    extension = ALLOWED_IMAGE_TYPES.get(file.content_type or "")
    if not extension:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La imagen debe ser JPG, PNG o WEBP.",
        )

    ProductService(db).get_by_id(product_id)
    filename = f"product-{product_id}-{uuid4().hex}{extension}"
    target = UPLOADS_DIR / filename

    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La imagen no puede superar 5MB.",
        )
    target.write_bytes(content)

    dto = UpdateProductDTO(image_url=f"/uploads/products/{filename}")
    return ProductService(db).update(product_id, dto)


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
