# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config.settings import settings

# Supabase uses PostgreSQL — ensure the URL uses the asyncpg driver scheme:
# postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DBNAME
DATABASE_URL = settings.database_url

# Create async engine
# echo=False in production; set to True temporarily for SQL debugging
engine = create_async_engine(DATABASE_URL, echo=False)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


# Base class for ORM models
class Base(DeclarativeBase):
    pass


# Dependency to inject database session into routes
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session