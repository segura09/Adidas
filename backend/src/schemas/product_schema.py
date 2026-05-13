from pydantic import BaseModel, EmailStr, Field

class CreateProductSchema(BaseModel):
    nombre: str
    descripcion: str
    precio_base: float
    categoria_id: int
    activo: bool

class UpdateProductSchema(BaseModel):
    nombre: str
    descripcion: str
    precio_base: float
    categoria_id: int
    activo: bool

class GetProductSchema(BaseModel):
    nombre: str
    descripcion: str
    precio_base: float
    categoria_id: int
    activo: bool

class DeleteProductSchema(BaseModel):
    id: int