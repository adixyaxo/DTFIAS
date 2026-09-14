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


import sys
from sqlalchemy.pool import NullPool

engine_kwargs = {
    "echo": False,
    "connect_args": {
        "statement_cache_size": 0,
        "prepared_statement_cache_size": 0,
    },
}

if "pytest" in sys.modules or os.environ.get("PYTEST_CURRENT_TEST"):
    # Test mode: no pooling (avoids connection leaks between test cases)
    engine_kwargs["poolclass"] = NullPool
elif os.environ.get("VERCEL"):
    # Vercel serverless: no persistent worker process, so pooling is meaningless
    # and will cause "connection already closed" errors across cold starts.
    engine_kwargs["poolclass"] = NullPool
else:
    engine_kwargs.update({
        "pool_pre_ping": True,
        "pool_size": 10,           # keep 10 warm connections for Supabase TLS reuse
        "max_overflow": 20,        # allow 20 extra connections under burst load
        "pool_recycle": 300,       # recycle connections every 5 min to prevent staleness
        "pool_timeout": 10,        # fail fast rather than queuing for 30s (default)
    })

# Async engine
engine = create_async_engine(DATABASE_URL, **engine_kwargs)

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
