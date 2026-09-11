import asyncio
from sqlalchemy import text
from app.config.database import AsyncSessionLocal
from infrastructure.security.authentication.passwords import hash_password

async def update_superadmin_password():
    new_hash = hash_password("superadmin123")
    print(f"New hash: {new_hash}")
    async with AsyncSessionLocal() as db:
        await db.execute(
            text("UPDATE auth.users SET encrypted_password = :hash WHERE email = 'superadmin@gmail.com'"),
            {"hash": new_hash}
        )
        await db.commit()
        print("Updated superadmin password hash.")

if __name__ == "__main__":
    asyncio.run(update_superadmin_password())
