from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repositories.devolucion_repository import DevolucionRepository
from src.mappers.devolucion_mapper import devolucion_to_response # Tu futuro mapper

class DevolucionService:
    def __init__(self, db: Session):
        self.repo = DevolucionRepository(db)

    def request_return(self, usuario_id: int, compra_id: int, items_a_devolver: list[dict]) -> dict:
        # Validar que la compra exista y pertenezca al usuario (Regla de negocio)
        compra = self.repo.find_compra_by_id(compra_id)
        if not compra or compra.usuario_id != usuario_id:
            raise HTTPException(status_code=404, detail="Compra no encontrada.")

        # Creamos la devolución física en la DB
        devolucion = self.repo.create_devolucion(compra_id=compra_id, items=items_a_devolver)
        return devolucion_to_response(devolucion)

    def approve_return(self, devolucion_id: int) -> dict:
        devolucion = self.repo.find_by_id(devolucion_id)
        if not devolucion:
            raise HTTPException(status_code=404, detail="Devolución no encontrada.")
        
        if devolucion.estado != "pendiente":
            raise HTTPException(status_code=400, detail="Solo se pueden aprobar devoluciones pendientes.")

        devolucion_actualizada = self.repo.update_estado(devolucion, "aprobada")
        return devolucion_to_response(devolucion_actualizada)

    def reject_return(self, devolucion_id: int) -> dict:
        devolucion = self.repo.find_by_id(devolucion_id)
        if not devolucion:
            raise HTTPException(status_code=404, detail="Devolución no encontrada.")
        
        if devolucion.estado != "pendiente":
            raise HTTPException(status_code=400, detail="Solo se pueden rechazar devoluciones pendientes.")

        devolucion_actualizada = self.repo.update_estado(devolucion, "rechazada")
        return devolucion_to_response(devolucion_actualizada)

    def mark_return_reintegrated(self, devolucion_id: int) -> dict:
        devolucion = self.repo.find_by_id(devolucion_id)
        if not devolucion:
            raise HTTPException(status_code=404, detail="Devolución no encontrada.")
        
        if devolucion.estado != "aprobada":
            raise HTTPException(status_code=400, detail="La devolución debe estar 'aprobada' antes de ser reintegrada.")

        for item in devolucion.items:
            # Le sumamos la cantidad devuelta al stock actual de la variante del producto
            self.repo.increment_variant_stock(variante_id=item.variante_id, cantidad=item.cantidad)

        devolucion_actualizada = self.repo.update_estado(devolucion, "reintegrada")
        return devolucion_to_response(devolucion_actualizada)