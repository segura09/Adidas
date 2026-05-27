from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from src.db.connection import get_db
from src.routers.carrito_router import get_current_cliente_id
from src.schemas.resena_schema import ResenaCreate, ResenaResponse, ResenaSummaryResponse
from src.services.resena_service import ResenaService


router = APIRouter(prefix="/productos", tags=["Resenas"])


@router.post("/resenas", response_model=ResenaResponse, status_code=status.HTTP_201_CREATED)
def publicar_resena(
    data: ResenaCreate,
    db: Session = Depends(get_db),
    cliente_id: int = Depends(get_current_cliente_id),
):
    service = ResenaService(db)
    return service.to_response(service.create_or_update_review(cliente_id, data))


@router.post("/{producto_id}/resenas", response_model=ResenaResponse, status_code=status.HTTP_201_CREATED)
def publicar_resena_producto(
    producto_id: int,
    data: ResenaCreate,
    db: Session = Depends(get_db),
    cliente_id: int = Depends(get_current_cliente_id),
):
    data.producto_id = producto_id
    service = ResenaService(db)
    return service.to_response(service.create_or_update_review(cliente_id, data))


@router.get("/{producto_id}/resenas", response_model=List[ResenaResponse])
def listar_resenas_producto(producto_id: int, db: Session = Depends(get_db)):
    service = ResenaService(db)
    return service.list_reviews_by_product(producto_id)


@router.get("/{producto_id}/resenas/resumen", response_model=ResenaSummaryResponse)
def obtener_resumen_resenas(producto_id: int, db: Session = Depends(get_db)):
    service = ResenaService(db)
    return service.get_product_review_summary(producto_id)
