from pydantic import BaseModel

class CartItemResponseDTO(BaseModel):
    variante_id: int
    producto_nombre: str
    talle: str
    color: str
    precio_unitario: float
    cantidad: int
    subtotal: float

class CartResponseDTO(BaseModel):
    cliente_id: int
    items: list[CartItemResponseDTO]
    total: float