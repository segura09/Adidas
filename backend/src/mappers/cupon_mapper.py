from src.dtos.cupon_dto import CuponResponseDTO


class CuponMapper:
    def to_cupon_response(self, cupon) -> CuponResponseDTO:
        return CuponResponseDTO.model_validate(cupon)
