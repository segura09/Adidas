
from fastapi import APIRouter, Depends, HTTPException
from src.schemas.carrito_schema import ItemCarritoAdd
from src.dtos.carrito_dto import CartResponseDTO
from src.repositories.carrito_repository import CarritoRepository
from src.services.carrito_service import CarritoService

# Reemplaza 'get_db' por el módulo/generador exacto que utilices en tu proyecto
from src.db.session import get_db 

router = APIRouter(prefix="/carrito", tags=["Carrito"])

# Fábrica de dependencias
def get_carrito_service(db = Depends(get_db)) -> CarritoService:
    repository = CarritoRepository(db)
    return CarritoService(repository)

# ID simulado (en el futuro vendrá del payload de un token JWT)
CLIENTE_MOCK_ID = 1

@router.post("/items", response_model=CartResponseDTO)
def add_item(
    data: ItemCarritoAdd, 
    service: CarritoService = Depends(get_carrito_service)
):
    return service.add_item_to_cart(
        cliente_id=CLIENTE_MOCK_ID, 
        variante_id=data.variante_id, 
        cantidad=data.cantidad
    )

@router.get("/", response_model=CartResponseDTO)
def get_cart(service: CarritoService = Depends(get_carrito_service)):
    return service.get_cart(cliente_id=CLIENTE_MOCK_ID)

@router.delete("/items")
def clear_cart(service: CarritoService = Depends(get_carrito_service)):
    return service.clear_cart(cliente_id=CLIENTE_MOCK_ID)

@router.post("/checkout")
def checkout(service: CarritoService = Depends(get_carrito_service)):
    return service.checkout_from_cart(cliente_id=CLIENTE_MOCK_ID)