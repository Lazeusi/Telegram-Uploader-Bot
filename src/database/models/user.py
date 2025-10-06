from src.database.connection import db
from datetime import datetime

class User:
    collection = db.users
    
    @classmethod
    async def create(cls , data : dict):
        # Create a new user in the database
        data["creaded_at"] = datetime.utcnow()
        await cls.collection.insert_one(data)
        
    @classmethod
    async def exists(cls , user_id : int) -> bool:
        return await cls.collection.find_one({"user_id" : user_id} , {"_id" : 0})
        
    @classmethod
    async def get(cls , user_id : int):
        return await cls.collection.find_one({"user_id" : user_id} , {"_id" : 0})
    
    @classmethod
    async def update(cls , user_id : int , data : dict):
        return await cls.collection.update_one({"user_id" : user_id} , {"$set" : data})
    
    @classmethod
    async def delete(cls , user_id : int):
        return await cls.collection.delete_one({"user_id" : user_id})
    

    @classmethod
    async def all(cls):
        # get all users
        cursor = cls.collection.find({} , {"_id" : 0})
        return [doc async for doc in cursor]