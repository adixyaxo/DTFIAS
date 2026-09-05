from sqlalchemy import select
from app.config.database import get_db
from app.models.test import Test

async def databaseTest():
    test = []
    async for db in get_db():
        result = await db.execute(select(Test))
        test:list[Test] = result.scalars().all()
    return test
