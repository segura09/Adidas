from fastapi import APIRouter, Depends, HTTPException, Query

from src.db.connection import get_db
from src.repositories.variante_repository import VarianteRepository
from src.schemas.variante_schema import StockUpdate, VarianteCreate, VarianteResponse
from src.services.variante_service import VarianteService


router = APIRouter(prefix="/variantes", tags=["Variantes"])


def get_variante_service(db=Depends(get_db)) -> VarianteService:
    return VarianteService(VarianteRepository(db))


@router.get("/stock-bajo")
def get_low_stock(
    umbral: int = Query(default=5, ge=0),
    service: VarianteService = Depends(get_variante_service),
):
    return service.get_low_stock_variants(umbral=umbral)


@router.post("/", response_model=VarianteResponse)
def create_variant(
    data: VarianteCreate,
    service: VarianteService = Depends(get_variante_service),
):
    return service.create_variant(data)


@router.get("/producto/{producto_id}", response_model=list[VarianteResponse])
def list_variants_by_product(
    producto_id: int,
    service: VarianteService = Depends(get_variante_service),
):
    return service.list_variants_by_product(producto_id)


@router.put("/{variante_id}/stock", response_model=VarianteResponse)
def update_stock(
    variante_id: int,
    data: StockUpdate,
    service: VarianteService = Depends(get_variante_service),
):
    variante = service.update_stock(variante_id, data.stock)
    if not variante:
        raise HTTPException(status_code=404, detail="Variante no encontrada")

    return variante
