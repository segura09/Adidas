from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repositories.cliente_repository import ClienteRepository
from src.mappers.compra_mapper import compra_to_response # Tu mapper original

class ClienteService:
    def __init__(self, db: Session):
        self.repo = ClienteRepository(db)

def get_customer_purchases(self, cliente_id: int, estado: str | None = None) -> list[dict]:

        cliente = self.repo.find_by_id(cliente_id)
        if not cliente:
            raise HTTPException(
                status_code=404,
                detail=f"Usuario con ID {cliente_id} no encontrado."
            )
            

        compras_db = self.repo.get_purchases(usuario_id=cliente_id, estado=estado)
        
 
        if not compras_db:
            return []
            
        try:

            resultado = [compra_to_response(compra) for compra in compras_db]
            if resultado is None:
                return []
            return resultado
            
        except Exception as e:
            
            print(f"Error en el mapper: {e}")
            return []