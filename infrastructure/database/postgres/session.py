# infrastructure/database/postgres/session.py
"""
Asynchronous PostgreSQL / Supabase connection and session factory.
Lives in infrastructure/ to uphold DDD layer boundaries (infrastructure does not import app).
"""
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL", "")
# Ensure asyncpg driver prefix
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Async engine
engine = create_async_engine(
    DATABASE_URL or "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres",
    echo=False,
    pool_pre_ping=True,
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Declarative Base for all ORM models
class Base(DeclarativeBase):
    pass

async def get_db():
    """Dependency for yielding an async database session."""
    async with AsyncSessionLocal() as session:
        yield session

__all__ = ["engine", "AsyncSessionLocal", "Base", "get_db"]
