from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.db.connection import get_db
from src.dtos.cupon_dto import CreateCuponDTO, CuponResponseDTO
from src.repositories.cupon_repository import CuponRepository
from src.schemas.cupon_schema import CreateCuponSchema
from src.services.cupon_sevice import CuponService


router = APIRouter(prefix="/cupones", tags=["Cupones"])


def get_service(db: Session = Depends(get_db)) -> CuponService:
    return CuponService(CuponRepository(db))


@router.get("", response_model=list[CuponResponseDTO])
@router.get("/", response_model=list[CuponResponseDTO])
def list_coupons(service: CuponService = Depends(get_service)):
    return service.list_all()


@router.post("", response_model=CuponResponseDTO, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=CuponResponseDTO, status_code=status.HTTP_201_CREATED)
def create_coupon(payload: CreateCuponSchema, service: CuponService = Depends(get_service)):
    return service.create_coupon(CreateCuponDTO(**payload.model_dump()))


@router.post("/validar")
def validate_coupon(payload: dict, service: CuponService = Depends(get_service)):
    cupon = service.validate_coupon(str(payload.get("codigo", "")).strip())
    return {
        "valido": True,
        "porcentaje_descuento": cupon.porcentaje_descuento,
        "cupon": cupon,
    }


@router.delete("/{cupon_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coupon(cupon_id: int, service: CuponService = Depends(get_service)):
    service.delete_coupon(cupon_id)
    return
