from datetime import datetime, time

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.db.connection import get_db
from src.services.compra_service import CompraService


router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/facturacion")
def get_billing_report(
    desde: str = Query(...),
    hasta: str = Query(...),
    db: Session = Depends(get_db),
):
    desde_dt = datetime.combine(datetime.fromisoformat(desde).date(), time.min)
    hasta_dt = datetime.combine(datetime.fromisoformat(hasta).date(), time.max)
    report = CompraService(db).get_billing_report(desde_dt, hasta_dt)
    return {
        "desde": desde,
        "hasta": hasta,
        "total_facturado": report["total_facturado"],
        "cantidad_compras": report["cantidad_compras"],
        "por_categoria": [
            {
                "categoria_id": item.get("categoria_id", 0),
                "nombre": item.get("nombre") or item.get("categoria"),
                "total": item["total"],
            }
            for item in report["desglose_por_categoria"]
        ],
    }
