"""
Quick DB connection test — runs outside FastAPI.
Usage: python scripts/test_db_connection.py
"""
import asyncio
import os
import sys

# Force UTF-8 output on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Make sure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")

async def test_connection():
    print(f"\n[DB TEST] Testing connection to:\n    {DATABASE_URL[:80]}...\n")

    try:
        import asyncpg
        # asyncpg expects postgresql:// not postgresql+asyncpg://
        raw_url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
        conn = await asyncpg.connect(raw_url, timeout=10)
        version = await conn.fetchval("SELECT version();")
        print(f"[OK] Connected!\n     Server: {version[:100]}")

        # Quick sanity checks
        tables = await conn.fetch(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
            """
        )
        if tables:
            print(f"\n[INFO] Tables in public schema ({len(tables)} found):")
            for row in tables:
                print(f"    - {row['table_name']}")
        else:
            print("\n[INFO] No tables found in public schema yet (fresh database).")

        await conn.close()
        print("\n[OK] Connection closed cleanly. DB is reachable.\n")

    except ImportError:
        print("[ERROR] asyncpg is not installed. Run: pip install asyncpg")
    except Exception as e:
        print(f"[ERROR] Connection FAILED: {type(e).__name__}: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_connection())
