from pydantic import BaseModel
from typing import List


class CheckoutItemSchema(BaseModel):
    variante_id: int
    cantidad: int


class CheckoutSchema(BaseModel):
    usuario_id: int = 1
    items: List[CheckoutItemSchema] = []
    codigo_cupon: str | None = None
    cupon_codigo: str | None = None
