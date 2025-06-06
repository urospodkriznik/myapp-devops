from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    
class ItemCreate(BaseModel):
    name: str
    description: str
    price: float