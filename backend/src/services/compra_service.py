from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.repositories.compra_repository import CompraRepository


class CompraService:

    def __init__(self, db: Session):

        self.db = db

        self.repository = CompraRepository(db)

    def validate_stock_for_items(
        self,
        items
    ):

        variants = []

        for item in items:

            variant = self.repository.get_variant_by_id(
                item.variante_id
            )

            if not variant:

                raise HTTPException(
                    status_code=404,
                    detail=f"Variante {item.variante_id} no encontrada"
                )

            if variant.stock < item.cantidad:

                raise HTTPException(
                    status_code=400,
                    detail=f"Stock insuficiente para variante {variant.id}"
                )

            variants.append({
                "variant": variant,
                "cantidad": item.cantidad
            })

        return variants

    def calculate_total(
        self,
        variants
    ):

        total = 0

        for item in variants:

            subtotal = (
                item["variant"].precio *
                item["cantidad"]
            )

            total += subtotal

        return total

    def create_purchase(
        self,
        data
    ):

        try:

            variants = self.validate_stock_for_items(
                data.items
            )

            total = self.calculate_total(
                variants
            )

            compra = self.repository.create_purchase(
                usuario_id=data.usuario_id,
                total=total
            )

            purchase_items = []

            for item in variants:

                variant = item["variant"]

                cantidad = item["cantidad"]

                subtotal = (
                    variant.precio *
                    cantidad
                )

                purchase_items.append({
                    "variante_id": variant.id,
                    "cantidad": cantidad,
                    "precio_unitario": variant.precio,
                    "subtotal": subtotal
                })

                self.repository.reserve_stock(
                    variant,
                    cantidad
                )

            self.repository.save_purchase_items(
                compra.id,
                purchase_items
            )

            self.db.commit()

            self.db.refresh(compra)

            return compra

        except Exception as e:

            self.db.rollback()

            raise e