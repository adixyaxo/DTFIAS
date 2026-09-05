# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import URL
from app.config.settings import settings, env

DATABASE_URL = URL.create(
    drivername="mysql+aiomysql",
    username=env.database.db_user,
    password=env.database.db_password,
    host=env.database.db_host,
    port=env.database.db_port,
    database=env.database.db_name
)

# Create async engine with connection pooling
engine = create_async_engine(DATABASE_URL, pool_size=10, max_overflow=5)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Base class for ORM models
class Base(DeclarativeBase):
    pass

# Dependency to inject database session into routes
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session   