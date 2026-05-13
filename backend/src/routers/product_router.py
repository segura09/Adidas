from fastapi import APIRouter, Query
from backend.src.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])

product_service = ProductService()


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
