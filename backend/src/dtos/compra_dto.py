from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PurchaseItemDTO(BaseModel):
    variante_id: int
    cantidad: int

class CreatePurchaseDTO(BaseModel):
    usuario_id: int
    items: List[PurchaseItemDTO]


class ItemCompraResponseDTO(BaseModel):
    producto_id: Optional[int] = None
    variante_id: int
    cantidad: int
    precio_unitario: float
    subtotal: float
    producto_nombre: Optional[str] = None
    talle: Optional[str] = None
    color: Optional[str] = None

    model_config = {"from_attributes": True}

class CompraConItemsResponseDTO(BaseModel):
    id: int
    cliente_id: int
    fecha: datetime
    total: float
    subtotal: float = 0
    descuento: float = 0
    estado: str
    cupon_codigo: Optional[str] = None
    items: List[ItemCompraResponseDTO] 

    model_config = {"from_attributes": True}
