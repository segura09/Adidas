from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session

from src.db.connection import get_db
from src.dtos.cliente_dto import CreateClienteDTO, ClienteResponseDTO, UpdateClienteDTO
from src.schemas.cliente_schema import CreateClienteSchema, UpdateClienteSchema
from src.dtos.compra_dto import CompraConItemsResponseDTO 
from src.services.cliente_service import ClienteService

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("/{cliente_id}/compras")
def get_customer_purchases(
    cliente_id: int, 
    estado: str | None = Query(None, description="Filtrar por estado de la compra"),
    db: Session = Depends(get_db)
):
    return ClienteService(db).get_customer_purchases(cliente_id=cliente_id, estado=estado)


@router.post("/", response_model=ClienteResponseDTO, status_code=status.HTTP_201_CREATED)
def create_cliente(payload: CreateClienteSchema, db: Session = Depends(get_db)):
    dto = CreateClienteDTO(**payload.model_dump())
    return ClienteService(db).create(dto)


@router.put("/{cliente_id}", response_model=ClienteResponseDTO)
def update_cliente(cliente_id: int, payload: UpdateClienteSchema, db: Session = Depends(get_db)):
    """Actualiza los datos de un cliente existente."""
    dto = UpdateClienteDTO(**payload.model_dump(exclude_unset=True))
    return ClienteService(db).update(cliente_id, dto)


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Borra (o da de baja) un cliente del sistema."""
    ClienteService(db).delete(cliente_id)
    return