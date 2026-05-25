from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.connection import get_db
from src.db.models.carrito_model import CarritoItem
from src.dtos.compra_dto import CompraConItemsResponseDTO
from src.mappers.compra_mapper import compra_to_response
from src.schemas.checkout_schema import CheckoutItemSchema, CheckoutSchema
from src.services.compra_service import CompraService


router = APIRouter(prefix="/compras", tags=["Compras"])
CLIENTE_MOCK_ID = 1


@router.post("", response_model=CompraConItemsResponseDTO)
@router.post("/", response_model=CompraConItemsResponseDTO)
def create_purchase(data: CheckoutSchema, db: Session = Depends(get_db)):
    if not data.items:
        cart_items = db.query(CarritoItem).filter(CarritoItem.cliente_id == CLIENTE_MOCK_ID).all()
        if not cart_items:
            raise HTTPException(status_code=400, detail="El carrito esta vacio")
        data.usuario_id = CLIENTE_MOCK_ID
        data.items = [
            CheckoutItemSchema(variante_id=item.variante_id, cantidad=item.cantidad)
            for item in cart_items
        ]

    compra = CompraService(db).create_purchase(data)
    db.query(CarritoItem).filter(CarritoItem.cliente_id == data.usuario_id).delete()
    db.commit()
    db.refresh(compra)
    return compra_to_response(compra)


@router.get("/{compra_id}", response_model=CompraConItemsResponseDTO)
def get_purchase(compra_id: int, db: Session = Depends(get_db)):
    compra = CompraService(db).repository.get_by_id(compra_id)
    if not compra:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    return compra_to_response(compra)


@router.post("/{compra_id}/pagar", response_model=CompraConItemsResponseDTO)
@router.put("/{compra_id}/pagar", response_model=CompraConItemsResponseDTO)
def mark_purchase_as_paid(compra_id: int, db: Session = Depends(get_db)):
    compra = CompraService(db).mark_purchase_as_paid(compra_id)
    return compra_to_response(compra)


@router.post("/{compra_id}/enviar", response_model=CompraConItemsResponseDTO)
@router.put("/{compra_id}/enviar", response_model=CompraConItemsResponseDTO)
def mark_purchase_as_shipped(compra_id: int, db: Session = Depends(get_db)):
    compra = CompraService(db).mark_purchase_as_shipped(compra_id)
    return compra_to_response(compra)


@router.post("/{compra_id}/entregar", response_model=CompraConItemsResponseDTO)
@router.put("/{compra_id}/entregar", response_model=CompraConItemsResponseDTO)
def mark_purchase_as_delivered(compra_id: int, db: Session = Depends(get_db)):
    compra = CompraService(db).mark_purchase_as_delivered(compra_id)
    return compra_to_response(compra)


@router.post("/{compra_id}/cancelar", response_model=CompraConItemsResponseDTO)
@router.put("/{compra_id}/cancelar", response_model=CompraConItemsResponseDTO)
def mark_purchase_as_cancelled(compra_id: int, db: Session = Depends(get_db)):
    compra = CompraService(db).mark_purchase_as_cancelled(compra_id)
    return compra_to_response(compra)
