import enum
from sqlalchemy import Column, Integer, String, Float, Enum as SqlEnum
from app.db import Base

class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SqlEnum(RoleEnum, name="userrole"), nullable=False, default=RoleEnum.USER)

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    description = Column(String(300))
    price = Column(Float)