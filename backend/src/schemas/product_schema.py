from pydantic import BaseModel, Field

class CreateProductSchema(BaseModel):
    nombre: str = Field(..., min_length=2)
    descripcion: str | None = Field(None)
    precio_base: float = Field(..., gt=0)
    categoria_id: int
    activo: bool = True

class UpdateProductSchema(BaseModel):
    nombre: str | None = Field(None, min_length=2)
    descripcion: str | None = Field(None)
    precio_base: float | None = Field(None, gt=0)
    categoria_id: int | None = Field(None)
    activo: bool | None = Field(None)

class GetProductSchema(BaseModel):
    id: int 
    nombre: str
    descripcion: str | None
    precio_base: float
    categoria_id: int
    activo: bool

    class Config:
        from_attributes = True

class DeleteProductSchema(BaseModel):
    id: int