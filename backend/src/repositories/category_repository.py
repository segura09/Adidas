from sqlalchemy.orm import Session

from src.db.models.category_model import Category


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, nombre: str, descripcion: str) -> Category:
        category = Category(nombre=nombre, descripcion=descripcion)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
