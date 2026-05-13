from datetime import datetime
from pydantic import BaseModel


class CreateCategoryDTO(BaseModel):
    nombre: str
    descripcion: str

class GetCategoryDTO(BaseModel):
    id: int

class CategoryResponseDTO(BaseModel):
    id: int
    nombre: str
    descripcion: str
    created_at: datetime

    model_config = {"from_attributes": True}
