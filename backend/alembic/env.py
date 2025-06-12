from dotenv import load_dotenv
load_dotenv()

import os
from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context
from app.db import Base
import app.models

# Load and convert URL
DATABASE_URL = os.getenv("DATABASE_URL")
SQLALCHEMY_URL = DATABASE_URL.replace("asyncpg", "psycopg2")

# Alembic config
config = context.config
fileConfig(config.config_file_name)
config.set_main_option("sqlalchemy.url", SQLALCHEMY_URL)

target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=SQLALCHEMY_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(SQLALCHEMY_URL, future=True)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()