from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from src.dtos.cliente_dto import CreateClienteDTO, ClienteResponseDTO, UpdateClienteDTO
from src.dtos.compra_dto import CompraConItemsResponseDTO
from src.repositories.cliente_repository import ClienteRepository
from src.mappers.compra_mapper import compra_to_response

class ClienteService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ClienteRepository(db)

    def create(self, dto: CreateClienteDTO) -> ClienteResponseDTO:
        try:
            cliente = self.repo.create(
                nombre=dto.nombre,
                email=dto.email,
                direccion=dto.direccion,
            )
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un cliente con ese email.",
            )
        return ClienteResponseDTO.model_validate(cliente)

    def list_all(self) -> list[ClienteResponseDTO]:
        return [ClienteResponseDTO.model_validate(cliente) for cliente in self.repo.list_all()]

    def update(self, cliente_id: int, dto: UpdateClienteDTO) -> ClienteResponseDTO:
        fields = dto.model_dump(exclude_unset=True)
        try:
            cliente = self.repo.update(cliente_id, **fields)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un cliente con ese email.",
            )
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado.")
        return ClienteResponseDTO.model_validate(cliente)

    def delete(self, cliente_id: int) -> None:
        try:
            deleted = self.repo.delete(cliente_id)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar un cliente con compras asociadas.",
            )
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado.")

    def get_customer_purchases(
        self,
        cliente_id: int,
        estado: str | None = None,
    ) -> list[CompraConItemsResponseDTO]:
        cliente = self.repo.find_by_id(cliente_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {cliente_id} no encontrado."
            )

        compras_db = self.repo.get_purchases(cliente_id=cliente_id, estado=estado)
        return [
            CompraConItemsResponseDTO.model_validate(compra_to_response(compra))
            for compra in compras_db
        ]
