from src.database.connection import db
from datetime import datetime

class Channel:
    collection = db.channels
    
    @classmethod
    async def add(cls, channel_id: int, title: str , channel_username: str = None):
        data = {
            "channel_id": channel_id,
            "title": title,
            "channel_username": channel_username,
            "added_at": datetime.now()
        }
        await cls.collection.insert_one(data)
        
    async def remove(cls, channel_id: int):
        await cls.collection.delete_one({"channel_id": channel_id})
        
    async def get_all(cls):
        channels = []
        cursor = cls.collection.find({})
        async for document in cursor:
            channels.append(document)
        return channels