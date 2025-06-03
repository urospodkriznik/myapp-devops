from sqlalchemy import Column, Integer, String, MetaData, Table
from app.db import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("email", String(100), unique=True),
)