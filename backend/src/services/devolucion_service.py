from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.mappers.devolucion_mapper import devolucion_to_response
from src.repositories.devolucion_repository import DevolucionRepository


class DevolucionService:
    def __init__(self, db: Session):
        self.repo = DevolucionRepository(db)

    def request_return(
        self,
        usuario_id: int,
        compra_id: int,
        items_a_devolver: list[dict],
        motivo: str | None = None,
    ) -> dict:
        compra = self.repo.find_compra_by_id(compra_id)
        if not compra or compra.cliente_id != usuario_id:
            raise HTTPException(status_code=404, detail="Compra no encontrada.")
        if compra.estado != "entregada":
            raise HTTPException(status_code=400, detail="Solo se pueden devolver compras entregadas.")
        if not items_a_devolver:
            raise HTTPException(status_code=400, detail="Seleccione al menos un item.")

        devolucion = self.repo.create_devolucion(
            compra_id=compra_id,
            items=items_a_devolver,
            motivo=motivo,
        )
        return devolucion_to_response(devolucion)

    def approve_return(self, devolucion_id: int) -> dict:
        devolucion = self.repo.find_by_id(devolucion_id)
        if not devolucion:
            raise HTTPException(status_code=404, detail="Devolucion no encontrada.")
        if devolucion.estado != "solicitada":
            raise HTTPException(status_code=400, detail="Solo se pueden aprobar devoluciones solicitadas.")
        return devolucion_to_response(self.repo.update_estado(devolucion, "aprobada"))

    def reject_return(self, devolucion_id: int) -> dict:
        devolucion = self.repo.find_by_id(devolucion_id)
        if not devolucion:
            raise HTTPException(status_code=404, detail="Devolucion no encontrada.")
        if devolucion.estado != "solicitada":
            raise HTTPException(status_code=400, detail="Solo se pueden rechazar devoluciones solicitadas.")
        return devolucion_to_response(self.repo.update_estado(devolucion, "rechazada"))

    def mark_return_reintegrated(self, devolucion_id: int) -> dict:
        devolucion = self.repo.find_by_id(devolucion_id)
        if not devolucion:
            raise HTTPException(status_code=404, detail="Devolucion no encontrada.")
        if devolucion.estado != "aprobada":
            raise HTTPException(status_code=400, detail="La devolucion debe estar aprobada.")

        for item in devolucion.items:
            self.repo.increment_variant_stock(variante_id=item.variante_id, cantidad=item.cantidad)

        return devolucion_to_response(self.repo.update_estado(devolucion, "reintegrada"))
