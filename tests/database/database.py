from infrastructure.database.postgres.connection import check_connection


async def databaseTest() -> bool:
    """Return True if Supabase/PostgreSQL is reachable."""
    return await check_connection()
