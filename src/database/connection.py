from motor.motor_asyncio import AsyncIOMotorClient
from src.config import settings

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URI)
        self.db = self.client[settings.DB_NAME]
        
        self.users = self.db["users"]
        
    async def test_connection(self):
        try:
            await self.client.admin.command('ping')
            print("Connected to MongoDB!")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            
db = Database()