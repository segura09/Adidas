from datetime import datetime

from pydantic import BaseModel


class CreateClienteDTO(BaseModel):
    nombre: str
    email: str
    direccion: str | None = None


class UpdateClienteDTO(BaseModel):
    nombre: str | None = None
    email: str | None = None
    direccion: str | None = None


class ClienteResponseDTO(BaseModel):
    id: int
    nombre: str
    email: str
    direccion: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
