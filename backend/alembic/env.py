from dotenv import load_dotenv
load_dotenv()

import os
from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context
from app.db import Base
import app.models

# Load DATABASE_URL from env
DATABASE_URL = os.getenv("DATABASE_URL")
# Convert asyncpg to psycopg2
SQLALCHEMY_URL = DATABASE_URL.replace("asyncpg", "psycopg2")

# Alembic config
config = context.config
fileConfig(config.config_file_name)
# Set URL into alembic config (this is the correct way!)
config.set_main_option("sqlalchemy.url", SQLALCHEMY_URL)

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    url = config.get_main_option("sqlalchemy.url")
    connectable = create_engine(url, future=True)

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