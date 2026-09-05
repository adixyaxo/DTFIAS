# infrastructure/database/postgres/connection.py
# Connection health check / diagnostics for the PostgreSQL/Supabase backend.
from sqlalchemy import text
from app.config.database import engine


async def check_connection() -> bool:
    """Returns True if the database is reachable, False otherwise."""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
