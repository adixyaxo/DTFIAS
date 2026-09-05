# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

# Load environment variables (e.g., DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
DATABASE_URL = (
    f"mysql+aiomysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST', '127.0.0.1')}:{os.getenv('DB_PORT', '3306')}"
    f"/{os.getenv('DB_NAME')}"
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