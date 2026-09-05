from tests.database.database import databaseTest
from app.schemas.test import Test
async def test():
    print("\n")
    print("Running Tests...")
    print("="*50)
    print("Testing Database Connection...")
    data:list[Test] = await databaseTest()
    if data[0]:
        print("Database Connection Test passed")
    else:
        print("Database Connection Test failed")
    print("="*50)

    
