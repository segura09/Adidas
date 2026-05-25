from pydantic import BaseModel, Field


class CreateCategorySchema(BaseModel):
    nombre: str = Field(min_length=1)
    descripcion: str | None = None

class UpdateCategorySchema(BaseModel):
    nombre: str | None = Field(None, min_length=3, max_length=50)
    descripcion: str | None = Field(None, max_length=255)

class GetCategorySchema(BaseModel):
    nombre: str
    descripcion: str | None

class DeleteCategorySchema(BaseModel):
    id: int
