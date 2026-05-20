from fastapi import APIRouter, Query, HTTPException
from backend.src.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])

product_service = ProductService()


# 1. Nueva Ruta: Productos más vendidos (HU9)
@router.get("/top")
def get_top_products(limit: int = Query(default=10, ge=1, le=50)):
    try:
        return product_service.get_top_selling_products(limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al obtener el reporte de productos top: {str(e)}"
        )


# 2. Rutas existentes
@router.get("/")
def list_products():
    return product_service.list_products()


@router.get("/search")
def search_products(
    categoria: int | None = Query(default=None),
    talle: str | None = Query(default=None),
    color: str | None = Query(default=None),
):
    return product_service.search_products(
        categoria=categoria,
        talle=talle,
        color=color,
    )