from pydantic import BaseModel, EmailStr, Field


class CreateCategorySchema(BaseModel):
    nombre: str = Field(min_length=1)
    descripcion: str
