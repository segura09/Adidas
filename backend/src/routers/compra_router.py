from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.connection import get_db
from src.dtos.compra_dto import CompraConItemsResponseDTO
from src.mappers.compra_mapper import compra_to_response
from src.schemas.checkout_schema import CheckoutSchema
from src.services.compra_service import CompraService


router = APIRouter(prefix="/compras", tags=["Compras"])


@router.post("/", response_model=CompraConItemsResponseDTO)
def create_purchase(data: CheckoutSchema, db: Session = Depends(get_db)):
    compra = CompraService(db).create_purchase(data)
    return compra_to_response(compra)


@router.put("/{compra_id}/pagar", response_model=CompraConItemsResponseDTO)
def mark_purchase_as_paid(compra_id: int, db: Session = Depends(get_db)):
    compra = CompraService(db).mark_purchase_as_paid(compra_id)
    return compra_to_response(compra)


@router.put("/{compra_id}/enviar", response_model=CompraConItemsResponseDTO)
def mark_purchase_as_shipped(compra_id: int, db: Session = Depends(get_db)):
    compra = CompraService(db).mark_purchase_as_shipped(compra_id)
    return compra_to_response(compra)


@router.put("/{compra_id}/entregar", response_model=CompraConItemsResponseDTO)
def mark_purchase_as_delivered(compra_id: int, db: Session = Depends(get_db)):
    compra = CompraService(db).mark_purchase_as_delivered(compra_id)
    return compra_to_response(compra)


@router.put("/{compra_id}/cancelar", response_model=CompraConItemsResponseDTO)
def mark_purchase_as_cancelled(compra_id: int, db: Session = Depends(get_db)):
    compra = CompraService(db).mark_purchase_as_cancelled(compra_id)
    return compra_to_response(compra)
