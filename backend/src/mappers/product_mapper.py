from src.dtos.product_dto import CreateProductDTO, ProductResponseDTO, UpdateProductDTO
from src.schemas.product_schema import CreateProductSchema, UpdateProductSchema

class ProductMapper:
    
    def to_product_response(product) -> ProductResponseDTO:

        return ProductResponseDTO(
            id=product.id,
            nombre=product.nombre,
            descripcion=product.descripcion,
            precio_base=product.precio_base,
            categoria_id=product.categoria_id,
            activo=product.activo
        )
    

    def create_schema_to_dto(schema: CreateProductSchema) -> CreateProductDTO:

        return CreateProductDTO(
            nombre=schema.nombre,
            descripcion=schema.descripcion,
            precio_base=schema.precio_base,
            categoria_id=schema.categoria_id,
            activo=schema.activo
        )

 
    def update_schema_to_dto(schema: UpdateProductSchema) -> UpdateProductDTO:

        return UpdateProductDTO(
            nombre=schema.nombre,
            descripcion=schema.descripcion,
            precio_base=schema.precio_base,
            categoria_id=schema.categoria_id,
            activo=schema.activo
        )