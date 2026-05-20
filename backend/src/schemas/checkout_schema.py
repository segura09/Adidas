from pydantic import BaseModel
from typing import List


class CheckoutItemSchema(BaseModel):
    variante_id: int
    cantidad: int


class CheckoutSchema(BaseModel):
    usuario_id: int
    items: List[CheckoutItemSchema]