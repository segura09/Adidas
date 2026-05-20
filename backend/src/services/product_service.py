from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.dtos.product_dto import CreateProductDTO, ProductResponseDTO, UpdateProductDTO
from src.mappers.product_mapper import to_product_response
from src.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, db: Session):
        self.repo = ProductRepository(db)

    def create(self, dto: CreateProductDTO) -> ProductResponseDTO:
        product = self.repo.create(
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            precio_base=dto.precio_base,
            categoria_id=dto.categoria_id,
            activo=dto.activo,
        )
        return to_product_response(product)

    def get_by_id(self, product_id: int) -> ProductResponseDTO:
        product = self.repo.find_by_id(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

        return to_product_response(product)

    def list_all(self) -> list[ProductResponseDTO]:
        return [to_product_response(product) for product in self.repo.list_all()]

    def update(self, product_id: int, dto: UpdateProductDTO) -> ProductResponseDTO:
        product = self.repo.update(product_id=product_id, **dto.model_dump(exclude_unset=True))
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

        return to_product_response(product)

    def delete(self, product_id: int) -> None:
        deleted = self.repo.delete(product_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    def search_products(
        self,
        categoria: int | None = None,
        talle: str | None = None,
        color: str | None = None,
    ) -> list[ProductResponseDTO]:
        products = self.repo.search_products(
            categoria=categoria,
            talle=talle,
            color=color,
        )
        return [to_product_response(product) for product in products]

    def get_top_selling_products(self, limit: int = 10) -> list[dict]:
        return self.repo.get_top_selling_products(limit=limit)
