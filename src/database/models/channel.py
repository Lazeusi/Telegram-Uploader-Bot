from src.database.connection import db


class Channel:
    collection = db.channels
    
    @classmethod 
    async def add(cls , identifier : str , title : str ,chat_type:str = "unknown"):
        data = {
            "identifier" : identifier,
            "title" : title,
            "chat_type" : chat_type,
        }
        await cls.collection.insert_one(data)
        
    @classmethod
    async def get_all(cls):
        channels = []
        cursor = cls.collection.find({})
        async for document in cursor:
            channels.append(document)
        return channels
    
    @classmethod
    async def delete(cls , idensifier : str):
        return await cls.collection.delete_one({"idensifier" : idensifier})
    
       