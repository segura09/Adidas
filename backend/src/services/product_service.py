from sqlalchemy.orm import Session

from src.dtos.product_dto import (
    CreateProductDTO,
    ProductResponseDTO,
)
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
        )

        return to_product_response(product)

    def get_by_id(self, product_id: int) -> ProductResponseDTO:
        # Nota: Cambié get_by_id por find_by_id ya que así se llama en tu Repository real
        product = self.repo.find_by_id(product_id)

        if not product:
            raise Exception("Producto no encontrado")

        return to_product_response(product)

    def list_all(self) -> list[ProductResponseDTO]:
        # Nota: Cambié list_all por list_all del repositorio
        products = self.repo.list_all()

        return [to_product_response(product) for product in products]

    def update(self, product_id: int, dto) -> ProductResponseDTO:
        product = self.repo.find_by_id(product_id)

        if not product:
            raise Exception("Producto no encontrado")

        updated_product = self.repo.update(
            product_id=product_id,
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            precio_base=dto.precio_base,
            categoria_id=dto.categoria_id,
            activo=dto.activo,
        )

        return to_product_response(updated_product)

    def delete(self, product_id: int) -> None:
        product = self.repo.find_by_id(product_id)

        if not product:
            raise Exception("Producto no encontrado")

        self.repo.delete(product_id)

    def search_products(
        self,
        categoria: int | None = None,
        talle: str | None = None,
        color: str | None = None,
    ):
        return self.repo.search_products(
            categoria=categoria,
            talle=talle,
            color=color,
        )

    # =========================================================================
    # AGREGADO: HU9 — Productos más vendidos
    # =========================================================================
    def get_top_selling_products(self, limit: int = 10) -> list[dict]:
        """
        Obtiene el ranking de productos más vendidos directamente procesado
        por el repositorio en forma de diccionarios/JSON.
        """
        return self.repo.get_top_selling_products(limit=limit)