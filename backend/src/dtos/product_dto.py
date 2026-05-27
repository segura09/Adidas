from datetime import datetime

from pydantic import BaseModel, Field


class CreateProductDTO(BaseModel):
    nombre: str
    descripcion: str | None = None
    image_url: str | None = None
    precio_base: float = Field(gt=0)
    categoria_id: int
    activo: bool = True


class UpdateProductDTO(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    image_url: str | None = None
    precio_base: float | None = Field(default=None, gt=0)
    categoria_id: int | None = None
    activo: bool | None = None


class ProductResponseDTO(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None
    image_url: str | None = None
    precio_base: float
    categoria_id: int
    activo: bool
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
