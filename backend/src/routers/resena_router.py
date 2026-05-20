# backend/src/routers/resena_router.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from src.db.session import get_db  # Dependencia de tu sesión de base de datos
from src.schemas.resena_schema import ResenaCreate, ResenaResponse, ResenaSummaryResponse
from src.services.resena_service import ResenaService
# from src.auth.dependencies import get_current_user  # Dependencia para el JWT

router = APIRouter(prefix="/productos", tags=["Reseñas"])

# Inyección dummy del ID del cliente (reemplazar por tu sistema real de JWT)
def get_current_cliente_id():
    return 1 

@router.post("/resenas", response_model=ResenaResponse, status_code=status.HTTP_201_CREATED)
def publicar_resena(
    data: ResenaCreate, 
    db: Session = Depends(get_db),
    cliente_id: int = Depends(get_current_cliente_id)
):
    """Crea o actualiza una reseña si el usuario ya posee el producto entregado."""
    service = ResenaService(db)
    return service.create_or_update_review(cliente_id, data)

@router.get("/{producto_id}/resenas", response_model=List[ResenaResponse])
def listar_resenas_producto(producto_id: int, db: Session = Depends(get_db)):
    """Devuelve la lista de las últimas reseñas asociadas a un producto."""
    service = ResenaService(db)
    return service.list_reviews_by_product(producto_id)

@router.get("/{producto_id}/resenas/resumen", response_model=ResenaSummaryResponse)
def obtener_resumen_resenas(producto_id: int, db: Session = Depends(get_db)):
    """Devuelve la cantidad de calificaciones y el promedio de puntaje de un producto."""
    service = ResenaService(db)
    return service.get_product_review_summary(producto_id)