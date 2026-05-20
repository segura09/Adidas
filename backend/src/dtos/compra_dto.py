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
    variante_id: int
    cantidad: int
    precio_unitario: float
    subtotal: float

    model_config = {"from_attributes": True}

class CompraConItemsResponseDTO(BaseModel):
    id: int
    cliente_id: int
    fecha: datetime
    total: float
    estado: str
    cupon_codigo: Optional[str] = None
    items: List[ItemCompraResponseDTO] 

    model_config = {"from_attributes": True}
