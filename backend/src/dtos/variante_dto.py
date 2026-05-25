from pydantic import BaseModel, Field


class CreateVarianteDTO(BaseModel):
    producto_id: int
    talle: str
    color: str
    stock: int = Field(ge=0)
    sku: str


class UpdateStockDTO(BaseModel):
    stock: int = Field(ge=0)


class VarianteResponseDTO(BaseModel):
    id: int
    producto_id: int
    talle: str
    color: str
    stock: int
    sku: str

    model_config = {"from_attributes": True}
