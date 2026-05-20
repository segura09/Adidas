from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload
from src.db.models.cliente_model import Cliente
from src.db.models.compra_model import Compra 

class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, nombre: str, email: str, direccion: str | None = None) -> Cliente:
        cliente = Cliente(nombre=nombre, email=email, direccion=direccion)
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def find_by_id(self, cliente_id: int) -> Cliente | None:
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def list_all(self) -> list[Cliente]:
        return self.db.query(Cliente).order_by(Cliente.id.asc()).all()

    def update(self, cliente_id: int, **fields) -> Cliente | None:
        cliente = self.find_by_id(cliente_id)
        if not cliente:
            return None

        for field, value in fields.items():
            setattr(cliente, field, value)

        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def delete(self, cliente_id: int) -> bool:
        cliente = self.find_by_id(cliente_id)
        if not cliente:
            return False

        self.db.delete(cliente)
        self.db.commit()
        return True

    def get_purchases(self, cliente_id: int, estado: str | None = None):
        query = (
            self.db.query(Compra)
            .options(selectinload(Compra.items))
            .filter(Compra.cliente_id == cliente_id)
        )
        
        if estado:
            query = query.filter(Compra.estado == estado)
            
        return query.order_by(Compra.created_at.desc()).all()
