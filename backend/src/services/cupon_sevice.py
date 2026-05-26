from datetime import date

from fastapi import HTTPException

from src.dtos.cupon_dto import CreateCuponDTO, CuponResponseDTO
from src.mappers.cupon_mapper import CuponMapper
from src.repositories.cupon_repository import CuponRepository


class CuponService:
    def __init__(self, repository: CuponRepository):
        self.repository = repository
        self.mapper = CuponMapper()

    def create_coupon(self, dto: CreateCuponDTO) -> CuponResponseDTO:
        dto.codigo = dto.codigo.strip().upper()
        existing = self.repository.find_by_codigo(dto.codigo)
        if existing:
            raise HTTPException(status_code=400, detail="El codigo de cupon ya existe.")

        new_cupon = self.repository.create(
            codigo=dto.codigo,
            porcentaje_descuento=dto.porcentaje_descuento,
            fecha_vencimiento=dto.fecha_vencimiento,
            usos_maximos=dto.usos_maximos,
        )
        return self.mapper.to_cupon_response(new_cupon)

    def list_all(self) -> list[CuponResponseDTO]:
        return [self.mapper.to_cupon_response(cupon) for cupon in self.repository.list_all()]

    def validate_coupon(self, codigo: str) -> CuponResponseDTO:
        codigo = codigo.strip().upper()
        cupon = self.repository.find_by_codigo(codigo)
        if not cupon:
            raise HTTPException(status_code=404, detail="Cupon no encontrado.")

        if cupon.fecha_vencimiento < date.today():
            raise HTTPException(status_code=400, detail="El cupon ha expirado.")

        if cupon.usos_actuales >= cupon.usos_maximos:
            raise HTTPException(status_code=400, detail="El cupon ha superado el limite de usos permitidos.")

        return self.mapper.to_cupon_response(cupon)

    def consume_coupon_use(self, codigo: str) -> CuponResponseDTO:
        codigo = codigo.strip().upper()
        self.validate_coupon(codigo)

        cupon = self.repository.find_by_codigo(codigo)
        updated_cupon = self.repository.increment_usage(cupon)
        return self.mapper.to_cupon_response(updated_cupon)

    def delete_coupon(self, cupon_id: int) -> None:
        deleted = self.repository.delete(cupon_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Cupon no encontrado.")
