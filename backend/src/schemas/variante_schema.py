from pydantic import BaseModel, Field


class VarianteCreate(BaseModel):
    producto_id: int
    talle: str
    color: str
    stock: int = Field(ge=0)
    sku: str


class VarianteResponse(BaseModel):
    id: int
    producto_id: int
    talle: str
    color: str
    stock: int
    sku: str


class StockUpdate(BaseModel):
    stock: int = Field(ge=0)