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

    def find_by_id(self, category_id: int) -> Category | None:
        return self.db.query(Category).filter(Category.id == category_id).first()
    
    def find_all(self) -> list[Category] | None:
        return self.db.query(Category).all()
    
    def update(self, category_id: int, **fields) -> Category | None:
        category = self.find_by_id(category_id)
        if category:
            for key, value in fields.items():
                if value is not None:
                    setattr(category, key, value)
            self.db.commit()
            self.db.refresh(category)
        return category

    def delete(self, category_id: int) -> bool:
        category = self.find_by_id(category_id)
        if category:
            self.db.delete(category)
            self.db.commit()
            return True
        return False
