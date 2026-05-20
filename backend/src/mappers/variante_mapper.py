from src.dtos.variante_dto import VarianteResponseDTO


def map_variante(variante) -> VarianteResponseDTO:
    return VarianteResponseDTO.model_validate(variante)
