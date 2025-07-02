from pydantic import BaseModel
from typing import Optional
from app.models import RoleEnum  # use only one source of truth

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: Optional[RoleEnum] = RoleEnum.USER

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: RoleEnum

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ItemCreate(BaseModel):
    name: str
    description: str
    price: float