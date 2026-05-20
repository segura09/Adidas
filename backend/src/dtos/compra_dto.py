from pydantic import BaseModel
from typing import List


class PurchaseItemDTO(BaseModel):
    variante_id: int
    cantidad: int


class CreatePurchaseDTO(BaseModel):
    usuario_id: int
    items: List[PurchaseItemDTO]