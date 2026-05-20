# backend/src/schemas/resena_schema.py

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class ResenaCreate(BaseModel):
    producto_id: int
    calificacion: int = Field(..., ge=1, le=5, description="La calificación debe ser entre 1 y 5")
    comentario: Optional[str] = Field(None, max_length=500)

class ResenaResponse(BaseModel):
    id: int
    cliente_id: int
    producto_id: int
    calificacion: int
    comentario: Optional[str]
    fecha_creacion: datetime

    class Config:
        from_attributes = True

class ResenaSummaryResponse(BaseModel):
    producto_id: int
    promedio_calificaciones: float
    total_resenas: int