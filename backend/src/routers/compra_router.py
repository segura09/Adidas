from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.db.connection import get_db
from src.db.models.carrito_model import CarritoItem
from src.dtos.compra_dto import CompraConItemsResponseDTO
from src.mappers.compra_mapper import compra_to_response
from src.routers.carrito_router import get_current_cliente_id
from src.schemas.checkout_schema import CheckoutItemSchema, CheckoutSchema
from src.services.compra_service import CompraService


router = APIRouter(prefix="/compras", tags=["Compras"])


@router.get("", response_model=list[CompraConItemsResponseDTO])
@router.get("/", response_model=list[CompraConItemsResponseDTO])
def list_purchases(
    estado: str | None = Query(None),
    db: Session = Depends(get_db),
):
    compras = CompraService(db).repository.list_all(estado=estado)
    return [compra_to_response(compra) for compra in compras]


@router.post("", response_model=CompraConItemsResponseDTO)
@router.post("/", response_model=CompraConItemsResponseDTO)
def create_purchase(
    data: CheckoutSchema,
    cliente_id: int = Depends(get_current_cliente_id),
    db: Session = Depends(get_db),
):
    if not data.items:
        cart_items = db.query(CarritoItem).filter(CarritoItem.cliente_id == cliente_id).all()
        if not cart_items:
            raise HTTPException(status_code=400, detail="El carrito esta vacio")
        data.items = [
            CheckoutItemSchema(variante_id=item.variante_id, cantidad=item.cantidad)
            for item in cart_items
        ]

    data.usuario_id = cliente_id
    compra = CompraService(db).create_purchase(data)
    db.query(CarritoItem).filter(CarritoItem.cliente_id == cliente_id).delete()
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
