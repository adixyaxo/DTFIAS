import asyncio
import os
import sys
import asyncpg
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "").replace("postgresql+asyncpg://", "postgresql://")

async def run_migration(file_path: str):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        sys.exit(1)
        
    with open(file_path, "r", encoding="utf-8") as f:
        sql = f.read()

    print(f"Applying migration: {file_path}")
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        await conn.execute(sql)
        print("Migration applied successfully!")
    except Exception as e:
        print(f"Migration failed: {e}")
        sys.exit(1)
    finally:
        await conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/run_migration.py <path_to_sql_file>")
        sys.exit(1)
    asyncio.run(run_migration(sys.argv[1]))
