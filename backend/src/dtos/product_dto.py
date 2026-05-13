from typing import Optional

class CreateProductDTO:
    nombre: str
    descripcion: str
    precio_base: float
    categoria_id: int
    activo: bool

class UpdateProductDTO:
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_base: Optional[float] = None
    categoria_id: Optional[int] = None
    activo: Optional[bool] = None

class GetProductDTO:
    id: int
    nombre: str
    descripcion: str | None
    precio_base: float
    categoria_id: int
    activo: bool

class DeleteProductDTO:
    id: int

class ProductResponseDTO:
    id: int
    nombre: str
    descripcion: str
    precio_base: float
    categoria_id: int
    activo: bool