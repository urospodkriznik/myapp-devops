from pydantic import BaseModel, Field
from typing import Optional
from app.models import RoleEnum  # use only one source of truth

class UserCreate(BaseModel):
    name: str = Field(..., example="John Doe", description="Full name of the user")
    email: str = Field(..., example="john@example.com", description="User's email address")
    password: str = Field(..., example="strongpassword123", description="User's password")
    role: Optional[RoleEnum] = Field(RoleEnum.USER, example="USER", description="Role of the user (ADMIN or USER)")

class UserResponse(BaseModel):
    id: int = Field(..., example=1, description="User ID")
    name: str = Field(..., example="John Doe", description="Full name of the user")
    email: str = Field(..., example="john@example.com", description="User's email address")
    role: RoleEnum = Field(..., example="USER", description="Role of the user (ADMIN or USER)")

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str = Field(..., example="john@example.com", description="User's email address")
    password: str = Field(..., example="strongpassword123", description="User's password")

class TokenResponse(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", description="JWT access token")
    token_type: str = Field("bearer", example="bearer", description="Type of the token")

class ItemCreate(BaseModel):
    name: str = Field(..., example="Laptop", description="Name of the item")
    description: str = Field(..., example="A high-end gaming laptop", description="Description of the item")
    price: float = Field(..., example=1499.99, description="Price of the item in USD")