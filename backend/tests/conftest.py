import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
from sqlalchemy.pool import StaticPool

from app.db import Base
from app.main import create_app
from app.dependencies import get_db  # get it from dependencies, not main

DATABASE_URL = "sqlite+aiosqlite://"

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

async def override_get_db():
    async with TestSessionLocal() as session:
        yield session

@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    return app

@pytest.fixture(autouse=True, scope="function")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield

@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

@pytest.fixture
def client_sync(app):
    with TestClient(app) as c:
        yield c