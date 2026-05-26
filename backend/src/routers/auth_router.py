from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.db.connection import get_db
from src.dtos.auth_dto import LoginDTO, TokenDTO
from src.schemas.auth_schema import LoginSchema, RegisterSchema, TokenSchema
from src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenSchema)
def login(payload: LoginSchema, db: Session = Depends(get_db)):
    dto = LoginDTO(**payload.model_dump())
    token: TokenDTO = AuthService(db).login(dto)
    user = AuthService(db).repo.find_by_email(dto.email)
    return TokenSchema(
        **token.model_dump(),
        user={
            "id": user.id,
            "email": user.email,
            "isAdmin": user.is_admin,
        },
    )


@router.post("/register", response_model=TokenSchema, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterSchema, db: Session = Depends(get_db)):
    try:
        token, user = AuthService(db).register_cliente(**payload.model_dump())
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una cuenta con ese email.",
        )

    return TokenSchema(
        **token.model_dump(),
        user={
            "id": user.id,
            "email": user.email,
            "isAdmin": user.is_admin,
        },
    )
