import asyncio
from sqlalchemy import text
from infrastructure.database.postgres.session import engine

async def main():
    print('connecting...')
    try:
        async with engine.begin() as conn:
            print('connected!')
            await conn.execute(text('SELECT 1'))
            print('query done')
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
