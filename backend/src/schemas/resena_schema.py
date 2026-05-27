from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ResenaCreate(BaseModel):
    producto_id: int | None = None
    calificacion: int | None = Field(None, ge=1, le=5)
    puntaje: int | None = Field(None, ge=1, le=5)
    comentario: Optional[str] = Field(None, max_length=500)


class ResenaResponse(BaseModel):
    id: int
    cliente_id: int
    cliente_nombre: Optional[str] = None
    producto_id: int
    puntaje: int
    comentario: Optional[str]
    fecha: datetime


class ResenaSummaryResponse(BaseModel):
    producto_id: int | None = None
    promedio: float
    cantidad: int
