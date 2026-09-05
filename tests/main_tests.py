from tests.database.database import databaseTest


async def test():
    print("\n")
    print("Running Tests...")
    print("=" * 50)
    print("Testing Database Connection (Supabase/PostgreSQL)...")
    connected: bool = await databaseTest()
    if connected:
        print("✓ Database Connection Test passed")
    else:
        print("✗ Database Connection Test FAILED — check DATABASE_URL in .env")
    print("=" * 50)
