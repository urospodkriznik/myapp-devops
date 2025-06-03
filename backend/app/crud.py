from app.db import database
from app.models import users
from app.schemas import UserCreate

async def get_users():
    query = users.select()
    return await database.fetch_all(query)

async def create_user(user: UserCreate):
    query = users.insert().values(name=user.name, email=user.email)
    return await database.execute(query)