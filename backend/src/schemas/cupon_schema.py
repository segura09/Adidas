from pydantic import BaseModel, Field
from datetime import date

class CreateCuponSchema(BaseModel):
    codigo: str = Field(..., min_length=3, max_length=50)
    porcentaje_descuento: float = Field(..., ge=1.0, le=100.0)
    fecha_vencimiento: date
    usos_maximos: int = Field(default=1, ge=1)


class UpdateCuponSchema(BaseModel):
    codigo: str | None = Field(None, min_length=3, max_length=50)
    porcentaje_descuento: float | None = Field(None, ge=1.0, le=100.0)
    fecha_vencimiento: date | None = Field(None)
    usos_maximos: int | None = Field(None, ge=1)
    usos_actuales: int | None = Field(None, ge=0)


class GetCuponSchema(BaseModel):
    id: int
    codigo: str
    porcentaje_descuento: float
    fecha_vencimiento: date
    usos_maximos: int
    usos_actuales: int

    class Config:
        from_attributes = True