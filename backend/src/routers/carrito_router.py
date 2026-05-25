from fastapi import APIRouter, Depends

from src.db.connection import get_db
from src.dtos.carrito_dto import CartResponseDTO
from src.repositories.carrito_repository import CarritoRepository
from src.schemas.carrito_schema import ItemCarritoAdd
from src.services.carrito_service import CarritoService


router = APIRouter(prefix="/carritos", tags=["Carrito"])


def get_carrito_service(db=Depends(get_db)) -> CarritoService:
    return CarritoService(CarritoRepository(db))


# TODO: reemplazar por el cliente autenticado cuando se conecte JWT.
CLIENTE_MOCK_ID = 1


@router.post("/items", response_model=CartResponseDTO)
def add_item(
    data: ItemCarritoAdd,
    service: CarritoService = Depends(get_carrito_service),
):
    return service.add_item_to_cart(
        cliente_id=CLIENTE_MOCK_ID,
        variante_id=data.variante_id,
        cantidad=data.cantidad,
    )


@router.get("/me", response_model=CartResponseDTO)
@router.get("/", response_model=CartResponseDTO)
def get_cart(service: CarritoService = Depends(get_carrito_service)):
    return service.get_cart(cliente_id=CLIENTE_MOCK_ID)


@router.delete("/items/{variante_id}", response_model=CartResponseDTO)
def remove_item(variante_id: int, service: CarritoService = Depends(get_carrito_service)):
    return service.remove_item(cliente_id=CLIENTE_MOCK_ID, variante_id=variante_id)


@router.delete("/me")
@router.delete("/items")
def clear_cart(service: CarritoService = Depends(get_carrito_service)):
    return service.clear_cart(cliente_id=CLIENTE_MOCK_ID)


@router.post("/checkout")
def checkout(service: CarritoService = Depends(get_carrito_service)):
    return service.checkout_from_cart(cliente_id=CLIENTE_MOCK_ID)
