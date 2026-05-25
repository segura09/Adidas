# backend/src/services/resena_service.py

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.repositories.resena_repository import ResenaRepository
from src.schemas.resena_schema import ResenaCreate

class ResenaService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ResenaRepository(db)

    def create_or_update_review(self, cliente_id: int, data: ResenaCreate):
        try:
            if data.calificacion is None:
                data.calificacion = data.puntaje
            # 1. Regla de negocio: Validar que el producto haya sido comprado y entregado
            has_purchased = self.repository.has_delivered_purchase(cliente_id, data.producto_id)
            if not has_purchased:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Solo puedes dejar una reseña si compraste el producto y ya fue entregado."
                )

            # 2. Buscar si ya existe una reseña previa (Upsert lógico)
            existing_review = self.repository.get_by_cliente_and_producto(cliente_id, data.producto_id)
            
            if existing_review:
                existing_review.calificacion = data.calificacion
                existing_review.comentario = data.comentario
                resena = existing_review
            else:
                resena_dict = data.model_dump(exclude={"puntaje"})
                resena_dict["cliente_id"] = cliente_id
                resena = self.repository.create(resena_dict)

            self.db.commit()
            self.db.refresh(resena)
            return resena

        except HTTPException as http_ex:
            self.db.rollback()
            raise http_ex
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al procesar la reseña: {str(e)}"
            )

    def list_reviews_by_product(self, producto_id: int):
        return [self.to_response(resena) for resena in self.repository.list_by_producto(producto_id)]

    def get_product_review_summary(self, producto_id: int):
        summary = self.repository.get_summary_by_producto(producto_id)
        return {
            "producto_id": producto_id,
            "promedio": summary["promedio_calificaciones"],
            "cantidad": summary["total_resenas"],
        }

    def to_response(self, resena):
        return {
            "id": resena.id,
            "cliente_id": resena.cliente_id,
            "producto_id": resena.producto_id,
            "puntaje": resena.calificacion,
            "comentario": resena.comentario,
            "fecha": resena.fecha_creacion,
        }
