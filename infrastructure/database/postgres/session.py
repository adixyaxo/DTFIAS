# infrastructure/database/postgres/session.py
"""
Asynchronous PostgreSQL / Supabase connection and session factory.
Lives in infrastructure/ to uphold DDD layer boundaries (infrastructure does not import app).
"""
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from app.config.settings import DATABASE_URL

# Ensure asyncpg driver prefix
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)


# Async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    connect_args={
        "statement_cache_size": 0,
        "prepared_statement_cache_size": 0,
    }
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Declarative Base for all ORM models
class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)

async def get_db():
    """Dependency for yielding an async database session."""
    async with AsyncSessionLocal() as session:
        yield session

__all__ = ["engine", "AsyncSessionLocal", "Base", "get_db"]
