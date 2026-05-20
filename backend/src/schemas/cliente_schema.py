from pydantic import BaseModel, EmailStr, Field


class CreateClienteSchema(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    email: EmailStr
    direccion: str | None = None


class UpdateClienteSchema(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=150)
    email: EmailStr | None = None
    direccion: str | None = None
