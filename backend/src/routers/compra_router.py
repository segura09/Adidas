from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.connection import get_db

from src.schemas.checkout_schema import CheckoutSchema

from src.services.compra_service import CompraService
from src.mappers.compra_mapper import compra_to_response


router = APIRouter(
    prefix="/compras",
    tags=["Compras"]
)


@router.post("/")
def create_purchase(
    data: CheckoutSchema,
    db: Session = Depends(get_db)
):

    service = CompraService(db)

    compra = service.create_purchase(data)

    return compra_to_response(compra)