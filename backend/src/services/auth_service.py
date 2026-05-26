from sqlalchemy.orm import Session

from src.db.models.cliente_model import Cliente
from src.db.models.user_model import User
from src.dtos.auth_dto import LoginDTO, TokenDTO
from src.repositories.user_repository import UserRepository
from src.utils.hash import hash_password
from src.utils.errors import UnauthorizedError
from src.utils.hash import verify_password
from src.utils.jwt import create_access_token


class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def login(self, dto: LoginDTO) -> TokenDTO:
        user = self.repo.find_by_email(dto.email)
        if not user or not verify_password(dto.password, user.password_hash):
            raise UnauthorizedError("Invalid credentials")

        token = create_access_token({"sub": str(user.id), "email": user.email})
        return TokenDTO(access_token=token)

    def register_cliente(
        self,
        nombre: str,
        email: str,
        password: str,
        age: int,
        direccion: str | None = None,
    ) -> tuple[TokenDTO, User]:
        user = User(
            email=email,
            password_hash=hash_password(password),
            age=age,
            is_admin=False,
        )
        cliente = Cliente(nombre=nombre, email=email, direccion=direccion)

        self.repo.db.add(user)
        self.repo.db.add(cliente)
        self.repo.db.commit()
        self.repo.db.refresh(user)

        token = create_access_token({"sub": str(user.id), "email": user.email})
        return TokenDTO(access_token=token), user
