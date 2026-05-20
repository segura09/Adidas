from sqlalchemy.orm import Session
from src.db.models.resena_model import Resena # Asegúrate de que el nombre coincida con tu modelo

class ResenaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, usuario_id: int, producto_id: int, calificacion: int, comentario: str) -> Resena:
        """Crea una reseña físicamente en pgAdmin y la devuelve"""
        resena = Resena(
            usuario_id=usuario_id,
            producto_id=producto_id,
            calificacion=calificacion,
            comentario=comentario
        )
        self.db.add(resena)
        self.db.commit()
        self.db.refresh(resena)
        return resena

    def find_by_id(self, resena_id: int) -> Resena | None:
        """Busca una reseña específica por su ID único"""
        return self.db.query(Resena).filter(Resena.id == resena_id).first()

    def find_by_usuario_y_producto(self, usuario_id: int, producto_id: int) -> Resena | None:
        """Útil para validar si un usuario ya reseñó este producto (evita spam)"""
        return self.db.query(Resena).filter(
            Resena.usuario_id == usuario_id,
            Resena.producto_id == producto_id
        ).first()

    def list_by_producto(self, producto_id: int) -> list[Resena]:
        """Devuelve todas las reseñas de un producto específico"""
        return self.db.query(Resena).filter(Resena.producto_id == producto_id).all()

    def list_all(self) -> list[Resena]:
        """Devuelve absolutamente todas las reseñas del sistema (Siguiendo el ejemplo)"""
        return self.db.query(Resena).all()

    def update(self, resena_id: int, **fields) -> Resena | None:
        """Actualiza los campos dinámicos de la reseña y la devuelve actualizada"""
        resena = self.find_by_id(resena_id)
        if not resena:
            return None
        
        # Recorremos los campos pasados por kwargs (**fields) y los asignamos
        for key, value in fields.items():
            if hasattr(resena, key):
                setattr(resena, key, value)
                
        self.db.commit()
        self.db.refresh(resena)
        return resena

    def delete(self, resena_id: int) -> bool:
        """Borra la reseña. Devuelve True si la borró, False si no existía"""
        resena = self.find_by_id(resena_id)
        if not resena:
            return False
            
        self.db.delete(resena)
        self.db.commit()
        return True