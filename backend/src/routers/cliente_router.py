from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session

from src.db.connection import get_db
from src.dtos.cliente_dto import CreateClienteDTO, ClienteResponseDTO, UpdateClienteDTO
from src.dtos.compra_dto import CompraConItemsResponseDTO
from src.schemas.cliente_schema import CreateClienteSchema, UpdateClienteSchema
from src.services.cliente_service import ClienteService
from src.routers.carrito_router import get_current_cliente_id

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("/me/compras", response_model=list[CompraConItemsResponseDTO])
def get_my_purchases(
    estado: str | None = Query(None),
    cliente_id: int = Depends(get_current_cliente_id),
    db: Session = Depends(get_db)
):
    if estado == "pendiente":
        estado = "pendiente_pago"
    return ClienteService(db).get_customer_purchases(cliente_id=cliente_id, estado=estado)


@router.get("/{cliente_id}/compras", response_model=list[CompraConItemsResponseDTO])
def get_customer_purchases(
    cliente_id: int, 
    estado: str | None = Query(None),
    db: Session = Depends(get_db)
):
    return ClienteService(db).get_customer_purchases(cliente_id=cliente_id, estado=estado)


# ✨ NUEVO ENDPOINT: Listar todos los clientes del sistema
@router.get("/", response_model=list[ClienteResponseDTO])
def list_clientes(db: Session = Depends(get_db)):
    """Devuelve la lista completa de todos los clientes registrados."""
    return ClienteService(db).list_all()


@router.post("/", response_model=ClienteResponseDTO, status_code=status.HTTP_201_CREATED)
def create_cliente(payload: CreateClienteSchema, db: Session = Depends(get_db)):
    dto = CreateClienteDTO(**payload.model_dump())
    return ClienteService(db).create(dto)


@router.put("/{cliente_id}", response_model=ClienteResponseDTO)
def update_cliente(cliente_id: int, payload: UpdateClienteSchema, db: Session = Depends(get_db)):
    dto = UpdateClienteDTO(**payload.model_dump(exclude_unset=True))
    return ClienteService(db).update(cliente_id, dto)


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    ClienteService(db).delete(cliente_id)
    return
