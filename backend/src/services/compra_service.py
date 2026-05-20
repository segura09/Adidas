from datetime import datetime
from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.repositories.compra_repository import CompraRepository


class CompraService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = CompraRepository(db)

    def validate_stock_for_items(self, items):
        variants = []
        for item in items:
            variant = self.repository.get_variant_by_id(item.variante_id)

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

    def calculate_total(self, variants):
        total = 0
        for item in variants:
            # Nota: Aseguramos que el precio del producto venga desde su relación
            # según tu modelo anterior: variant.producto.precio_base
            precio = getattr(item["variant"], "precio", None) or item["variant"].producto.precio_base
            subtotal = precio * item["cantidad"]
            total += subtotal
        return total



    def apply_coupon_to_purchase(self, codigo_cupon: str):
        """Busca el cupón, valida vigencia y disponibilidad de usos."""
        cupon = self.repository.get_coupon_by_code(codigo_cupon)
        
        if not cupon:
            raise HTTPException(
                status_code=404,
                detail=f"El cupón '{codigo_cupon}' no existe."
            )
            
        if cupon.fecha_vencimiento < datetime.now():
            raise HTTPException(
                status_code=400,
                detail="El cupón ingresado ya ha vencido."
            )
            
        if cupon.usos_actuales >= cupon.usos_maximos:
            raise HTTPException(
                status_code=400,
                detail="El cupón ya no tiene usos disponibles."
            )
            
        return cupon

    def recalculate_total_with_discount(self, total: float, porcentaje_descuento: int) -> float:
        """Aplica el porcentaje de descuento al total original."""
        descuento = float(total) * (porcentaje_descuento / 100.0)
        total_final = float(total) - descuento
        return max(total_final, 0.0)

    def increment_coupon_use_on_confirm(self, cupon):
        """Suma un uso al cupón dentro de la transacción."""
        self.repository.increment_coupon_use(cupon)



    def create_purchase(self, data):
        try:
    
            variants = self.validate_stock_for_items(data.items)

            total = self.calculate_total(variants)
            
            cupon_id = None
            if hasattr(data, 'codigo_cupon') and data.codigo_cupon:
                cupon = self.apply_coupon_to_purchase(data.codigo_cupon)
                total = self.recalculate_total_with_discount(total, cupon.porcentaje_descuento)
                cupon_id = cupon.id


            compra = self.repository.create_purchase(
                usuario_id=data.usuario_id,
                total=total,
                cupon_id=cupon_id 
            )

            purchase_items = []
            for item in variants:
                variant = item["variant"]
                cantidad = item["cantidad"]
                precio_unitario = getattr(variant, "precio", None) or variant.producto.precio_base

                subtotal = precio_unitario * cantidad

                purchase_items.append({
                    "variante_id": variant.id,
                    "cantidad": cantidad,
                    "precio_unitario": precio_unitario,
                    "subtotal": subtotal
                })

                self.repository.reserve_stock(variant, cantidad)

            self.repository.save_purchase_items(
                compra.id,
                purchase_items
            )

            if cupon_id:
                self.increment_coupon_use_on_confirm(cupon)

            self.db.commit()
            self.db.refresh(compra)

            return compra

        except Exception as e:
            self.db.rollback()
            raise e