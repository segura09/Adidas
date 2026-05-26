from fastapi import APIRouter, Depends, HTTPException, status

from src.db.connection import get_db
from src.db.models.user_model import User
from src.dtos.carrito_dto import CartResponseDTO
from src.repositories.carrito_repository import CarritoRepository
from src.repositories.cliente_repository import ClienteRepository
from src.schemas.carrito_schema import ItemCarritoAdd
from src.services.carrito_service import CarritoService
from src.middlewares.auth_middleware import get_current_user


router = APIRouter(prefix="/carritos", tags=["Carrito"])


def get_carrito_service(db=Depends(get_db)) -> CarritoService:
    return CarritoService(CarritoRepository(db))


def get_current_cliente_id(
    user: User = Depends(get_current_user),
    db=Depends(get_db),
) -> int:
    cliente = ClienteRepository(db).find_by_email(user.email)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe un cliente asociado a este usuario.",
        )
    return cliente.id


@router.post("/items", response_model=CartResponseDTO)
def add_item(
    data: ItemCarritoAdd,
    cliente_id: int = Depends(get_current_cliente_id),
    service: CarritoService = Depends(get_carrito_service),
):
    return service.add_item_to_cart(
        cliente_id=cliente_id,
        variante_id=data.variante_id,
        cantidad=data.cantidad,
    )


@router.get("/me", response_model=CartResponseDTO)
@router.get("/", response_model=CartResponseDTO)
def get_cart(
    cliente_id: int = Depends(get_current_cliente_id),
    service: CarritoService = Depends(get_carrito_service),
):
    return service.get_cart(cliente_id=cliente_id)


@router.delete("/items/{variante_id}", response_model=CartResponseDTO)
def remove_item(
    variante_id: int,
    cliente_id: int = Depends(get_current_cliente_id),
    service: CarritoService = Depends(get_carrito_service),
):
    return service.remove_item(cliente_id=cliente_id, variante_id=variante_id)


@router.delete("/me")
@router.delete("/items")
def clear_cart(
    cliente_id: int = Depends(get_current_cliente_id),
    service: CarritoService = Depends(get_carrito_service),
):
    return service.clear_cart(cliente_id=cliente_id)


@router.post("/checkout")
def checkout(
    cliente_id: int = Depends(get_current_cliente_id),
    service: CarritoService = Depends(get_carrito_service),
):
    return service.checkout_from_cart(cliente_id=cliente_id)
