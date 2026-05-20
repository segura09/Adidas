from datetime import datetime
from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.db.models.compra_model import Compra
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
            precio = getattr(item["variant"], "precio", None) or item["variant"].producto.precio_base
            subtotal = precio * item["cantidad"]
            total += subtotal
        return total

    def apply_coupon_to_purchase(self, codigo_cupon: str):
        """Busca el cupón, valida vigencia y disponibilidad de usos (HU6)."""
        cupon = self.repository.get_coupon_by_code(codigo_cupon)
        
        if not cupon:
            raise HTTPException(
                status_code=404,
                detail=f"El cupón '{codigo_cupon}' no existe."
            )
            
        fecha_actual = datetime.now().date() if type(cupon.fecha_vencimiento) == type(datetime.now().date()) else datetime.now()
        if cupon.fecha_vencimiento < fecha_actual:
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
        """Aplica el porcentaje de descuento al total original (HU6)."""
        descuento = float(total) * (porcentaje_descuento / 100.0)
        total_final = float(total) - descuento
        return max(total_final, 0.0)

    def increment_coupon_use_on_confirm(self, cupon):
        """Suma un uso al cupón dentro de la transacción (HU6)."""
        self.repository.increment_coupon_use(cupon)

    def create_purchase(self, data):
        """Flujo principal de creación de compra unificado (HU5 + HU6)."""
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
                cupon_id=cupon_id,
                estado="pendiente_pago"
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

                # HU5/HU7: Se pre-reserva el stock preventivamente al crear la orden pendiente
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

        except HTTPException as http_ex:
            self.db.rollback()
            raise http_ex
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno del servidor: {str(e)}"
            )

    # --- NUEVAS FUNCIONES HU7 (GESTIÓN DE ESTADOS DE COMPRA) ---

    def mark_purchase_as_paid(self, compra_id: int):
        """Pasa la compra de 'pendiente' a 'pagada' (HU7)."""
        try:
            # Reutilizamos el repositorio para buscar la compra (puedes agregar este método simple en tu repo)
            compra = self.repository.get_by_id(compra_id)
            
            # Si prefieres una llamada directa y limpia para evitar problemas de búsqueda:
            if not compra:
                raise HTTPException(status_code=404, detail="Compra no encontrada")
            
            if compra.estado not in ["pendiente", "pendiente_pago"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail=f"No se puede pagar una compra en estado '{compra.estado}'"
                )
            
            # Nota de stock: Como el stock ya fue descontado preventivamente en create_purchase (reserve_stock),
            # al pagar simplemente confirmamos la transición de estado.
            compra.estado = "pagada"
            self.db.commit()
            self.db.refresh(compra)
            return compra
            
        except HTTPException as http_ex:
            self.db.rollback()
            raise http_ex
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def mark_purchase_as_cancelled(self, compra_id: int):
        """Cancela la compra. Devuelve el stock reservado al inventario (HU7)."""
        try:
            compra = self.db.query(Compra).filter(Compra.id == compra_id).first()
            if not compra:
                raise HTTPException(status_code=404, detail="Compra no encontrada")
            
            if compra.estado not in ["pendiente", "pendiente_pago", "pagada"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail=f"No se puede cancelar una compra en estado '{compra.estado}'"
                )
            
            # Como estuvo en pendiente o pagada, el stock fue retenido. Hay que restituirlo:
            for item in compra.items:
                variant = self.repository.get_variant_by_id(item.variante_id)
                if variant:
                    variant.stock += item.cantidad  # Devolvemos las unidades al inventario
            
            compra.estado = "cancelada"
            self.db.commit()
            self.db.refresh(compra)
            return compra
            
        except HTTPException as http_ex:
            self.db.rollback()
            raise http_ex
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    # --- NUEVA FUNCIÓN HU14 (REPORTE DE FACTURACIÓN) ---

    def get_billing_report(self, desde: datetime, hasta: datetime):
        """Genera el reporte consolidado de facturación (HU14)."""
        summary = self.repository.get_billing_summary(desde, hasta)
        desglose_categorias = self.repository.get_billing_by_category(desde, hasta)
        
        total_devoluciones = 0.0
        try:
            from src.db.models.devolucion_model import Devolucion
            total_devuelto = self.db.query(func.sum(Devolucion.total)).filter(
                Devolucion.fecha >= desde,
                Devolucion.fecha <= hasta,
                Devolucion.estado == "reintegrada"
            ).scalar()
            total_devoluciones = float(total_devuelto or 0.0)
        except ImportError:
            pass

        total_neto = max(summary["total_facturado"] - total_devoluciones, 0.0)

        return {
            "total_facturado": total_neto,
            "cantidad_compras": summary["cantidad_compras"],
            "desglose_por_categoria": desglose_categorias
        }

    def mark_purchase_as_shipped(self, compra_id: int):
        """Pasa la compra de 'pagada' a 'enviada'."""
        compra = self.repository.get_by_id(compra_id)
        if not compra or compra.estado != "pagada":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Solo se pueden enviar compras que ya estén pagadas"
            )
        return self.repository.update_estado(compra_id, "enviada")


    def mark_purchase_as_delivered(self, compra_id: int):
        """Pasa la compra de 'enviada' a 'entregada'."""
        compra = self.repository.get_by_id(compra_id)
        if not compra or compra.estado != "enviada":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Solo se pueden marcar como entregadas las compras enviadas"
            )
        return self.repository.update_estado(compra_id, "entregada")
