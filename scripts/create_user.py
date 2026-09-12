import asyncio
import os
import sys
import uuid
import asyncpg
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from infrastructure.security.authentication.passwords import hash_password
from app.config.settings import DATABASE_URL

RAW_DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")


async def create_user(full_name: str, employee_code: str, raw_password: str, role_name: str):
    hashed_password = hash_password(raw_password)
    new_user_id = str(uuid.uuid4())
    
    conn = await asyncpg.connect(RAW_DATABASE_URL)
    try:
        # Create user
        await conn.execute(
            """
            INSERT INTO profiles (id, full_name, employee_code, hashed_password, status) 
            VALUES ($1, $2, $3, $4, 'ACTIVE')
            ON CONFLICT (employee_code) DO UPDATE SET hashed_password = EXCLUDED.hashed_password
            """,
            new_user_id, full_name, employee_code, hashed_password
        )
        
        # Get role ID
        role_id = await conn.fetchval("SELECT id FROM roles WHERE name = $1", role_name)
        if not role_id:
            print(f"Error: Role {role_name} not found.")
            return

        # Fetch actual user ID (in case it existed and updated)
        user_id = await conn.fetchval("SELECT id FROM profiles WHERE employee_code = $1", employee_code)
        
        # Assign role
        await conn.execute(
            """
            INSERT INTO user_roles (user_id, role_id) VALUES ($1, $2)
            ON CONFLICT DO NOTHING
            """,
            user_id, role_id
        )
        print(f"Successfully created/updated user {employee_code} with role {role_name}")
    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python scripts/create_user.py <full_name> <employee_code> <password> <role_name>")
        sys.exit(1)
        
    asyncio.run(create_user(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
