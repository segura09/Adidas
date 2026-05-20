from datetime import date
from fastapi import HTTPException
from src.repositories.cupon_repository import CuponRepository
from src.mappers.cupon_mapper import CuponMapper
from src.dtos.cupon_dto import CreateCuponDTO, CuponResponseDTO

class CuponService:
    def __init__(self, repository: CuponRepository):
        self.repository = repository
        self.mapper = CuponMapper()

    def create_coupon(self, dto: CreateCuponDTO) -> CuponResponseDTO:
        """HU4: Crear cupón validando que el código sea único"""
        existing = self.repository.find_by_codigo(dto.codigo)
        if existing:
            raise HTTPException(status_code=400, detail="El código de cupón ya existe.")
        
        new_cupon = self.repository.create(
            codigo=dto.codigo,
            porcentaje_descuento=dto.porcentaje_descuento,
            fecha_vencimiento=dto.fecha_vencimiento,
            usos_maximos=dto.usos_maximos
        )
        return self.mapper.to_cupon_response(new_cupon)

    def validate_coupon(self, codigo: str) -> CuponResponseDTO:
        cupon = self.repository.find_by_codigo(codigo)
        if not cupon:
            raise HTTPException(status_code=404, detail="Cupón no encontrado.")

        # Validación de Fecha 
        if cupon.fecha_vencimiento < date.today():
            raise HTTPException(status_code=400, detail="El cupón ha expirado.")

        # Validación de cantidad de usos
        if cupon.usos_actuales >= cupon.usos_maximos:
            raise HTTPException(status_code=400, detail="El cupón ha superado el límite de usos permitidos.")

        return self.mapper.to_cupon_response(cupon)

    def consume_coupon_use(self, codigo: str) -> CuponResponseDTO:
        self.validate_coupon(codigo)
        
        cupon = self.repository.find_by_codigo(codigo)
        updated_cupon = self.repository.increment_usage(cupon)
        return self.mapper.to_cupon_response(updated_cupon)