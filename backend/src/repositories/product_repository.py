# TODO: implementar ProductRepository (create, find_by_id, list_all, update, delete)
# Seguí el patrón de user_repository.py

from sqlalchemy.orm import Session
from src.db.models.product_model import Product


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, nombre: str, descripcion: str, precio_base: float, categoria_id: int, activo: bool) -> Product:
        # Creamos la instancia con los campos reales de un producto
        product = Product(nombre=nombre, descripcion=descripcion, precio_base=precio_base, categoria_id=categoria_id, activo=activo)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def find_by_id(self, product_id: int) -> Product | None:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def list_all(self) -> list[Product]:
        return self.db.query(Product).all()

    def update(self, product_id: int, **fields) -> Product | None:
        product = self.find_by_id(product_id)
        if product:
            for key, value in fields.items():
                if value is not None:
                    setattr(product, key, value)
            self.db.commit()
            self.db.refresh(product)
        return product

    def delete(self, product_id: int) -> bool:
        product = self.find_by_id(product_id)
        if product:
            self.db.delete(product)
            self.db.commit()
            return True
        return False

