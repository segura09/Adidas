from pydantic import BaseModel, Field

class ItemCarritoAdd(BaseModel):
    variante_id: int = Field(..., description="ID de la variante específica (talle/color)")
    cantidad: int = Field(..., gt=0, description="La cantidad a añadir debe ser mayor a cero")