from sqlalchemy.orm import Session
from src.db.models.compra_model import Compra 

class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, usuario_id: int):
        """Busca si el usuario existe en pgAdmin"""
        from src.db.models.user_model import User 
        return self.db.query(User).filter(User.id == usuario_id).first()

    def get_purchases(self, usuario_id: int, estado: str | None = None):
        query = self.db.query(Compra).filter(Compra.usuario_id == usuario_id)
        
        if estado:
            query = query.filter(Compra.estado == estado)
            
        return query.order_by(Compra.created_at.desc()).all()