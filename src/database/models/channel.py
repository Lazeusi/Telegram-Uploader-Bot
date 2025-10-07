from src.database.connection import db


class Channel:
    collection = db.channels
    
    @classmethod
    async def add(cls , identifier : int , chat_type : str , title : str = None):
        existing = await cls.collection.find_one({"identifier": identifier})
        if not existing:
            await cls.collection.insert_one({
                "identifier": identifier,
                "chat_type": chat_type,
                "title": title
            })
            
    @classmethod
    async def get_all(cls):
        cursor = cls.collection.find({} , {"_id": 0})
        return [doc async for doc in cursor]
    
    @classmethod
    async def delete(cls , identifier : int):
        await cls.collection.delete_one({"identifier": identifier})
       