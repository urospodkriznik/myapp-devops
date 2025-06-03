from fastapi import FastAPI
from app import db, models, crud, schemas

app = FastAPI()

@app.get("/api/users")
async def get_users():
    return await crud.get_users()

@app.post("/api/users")
async def create_user(user: schemas.UserCreate):
    return await crud.create_user(user)