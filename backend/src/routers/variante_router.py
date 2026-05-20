from fastapi import APIRouter, Query, HTTPException, Depends
from src.schemas.variante_schema import (
    VarianteCreate,
    VarianteResponse,
    StockUpdate
)
from src.repositories.variante_repository import VarianteRepository
from src.services.variante_service import VarianteService

# IMPORTANTE: Reemplaza 'get_db' por la función real de tu proyecto 
# que maneja la conexión a tu base de datos nativa.
from src.db.session import get_db 

router = APIRouter(
    prefix="/variantes",
    tags=["Variantes"]
)

# Función auxiliar para inicializar el servicio con su repositorio y BD en cada request
def get_variante_service(db = Depends(get_db)) -> VarianteService:
    repository = VarianteRepository(db)
    return VarianteService(repository)


# =========================================================================
# NUEVO ENDPOINT: HU10 — Stock bajo
# =========================================================================
@router.get("/stock-bajo")
def get_low_stock(
    umbral: int = Query(default=5, ge=0),
    service: VarianteService = Depends(get_variante_service)
):
    try:
        return service.get_low_stock_variants(umbral=umbral)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener el reporte de stock bajo: {str(e)}"
        )


# =========================================================================
# RUTAS EXISTENTES (Actualizadas con inyección de dependencias real)
# =========================================================================

@router.post("/", response_model=VarianteResponse)
def create_variant(
    data: VarianteCreate, 
    service: VarianteService = Depends(get_variante_service)
):
    return service.create_variant(data)


@router.get("/producto/{producto_id}")
def list_variants_by_product(
    producto_id: int, 
    service: VarianteService = Depends(get_variante_service)
):
    return service.list_variants_by_product(producto_id)


@router.put("/{variante_id}/stock")
def update_stock(
    variante_id: int, 
    data: StockUpdate, 
    service: VarianteService = Depends(get_variante_service)
):
    return service.update_stock(
        variante_id,
        data.stock
    )