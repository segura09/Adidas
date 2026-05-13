from fastapi import APIRouter

from src.schemas.variante_schema import (
    VarianteCreate,
    VarianteResponse,
    StockUpdate
)

router = APIRouter(
    prefix="/variantes",
    tags=["Variantes"]
)

# ejemplo de dependencias
repository = None
service = None


@router.post("/", response_model=VarianteResponse)
def create_variant(data: VarianteCreate):
    return service.create_variant(data)


@router.get("/producto/{producto_id}")
def list_variants_by_product(producto_id: int):
    return service.list_variants_by_product(producto_id)


@router.put("/{variante_id}/stock")
def update_stock(variante_id: int, data: StockUpdate):
    return service.update_stock(
        variante_id,
        data.stock
    )