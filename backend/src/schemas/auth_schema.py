from pydantic import BaseModel, EmailStr, Field


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class RegisterSchema(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    email: EmailStr
    password: str = Field(min_length=8)
    age: int = Field(default=18, ge=18)
    direccion: str | None = None


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict | None = None
