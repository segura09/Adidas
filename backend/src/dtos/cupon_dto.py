from datetime import date

from pydantic import BaseModel, Field


class CreateCuponDTO(BaseModel):
    codigo: str
    porcentaje_descuento: float = Field(ge=1, le=100)
    fecha_vencimiento: date
    usos_maximos: int = Field(ge=1)


class CuponResponseDTO(BaseModel):
    id: int
    codigo: str
    porcentaje_descuento: float
    fecha_vencimiento: date
    usos_maximos: int
    usos_actuales: int

    model_config = {"from_attributes": True}
