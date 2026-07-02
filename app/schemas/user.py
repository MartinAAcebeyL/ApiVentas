import uuid
from datetime import date
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str = ""
    last_name: str = ""
    phone: str | None = None
    address: str | None = None
    birthday: date | None = None
    is_staff: bool = False


class UserRead(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_staff: bool
    phone: str | None
    address: str | None
    birthday: date | None
    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str
