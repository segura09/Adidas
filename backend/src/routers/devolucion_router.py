from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.connection import get_db
from src.services.devolucion_service import DevolucionService


router = APIRouter(prefix="/compras", tags=["Devoluciones"])
CLIENTE_MOCK_ID = 1


@router.post("/{compra_id}/devoluciones")
def request_return(compra_id: int, payload: dict, db: Session = Depends(get_db)):
    return DevolucionService(db).request_return(
        usuario_id=CLIENTE_MOCK_ID,
        compra_id=compra_id,
        items_a_devolver=payload.get("items", []),
        motivo=payload.get("motivo"),
    )
