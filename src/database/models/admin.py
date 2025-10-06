from datetime import datetime
from aiogram import Bot
from src.database.connection import db

from src.logger import logger
class Admin:
    user_collection = db.admins
    
    @classmethod
    async def add(cls , user_id : int , username : str = None):
        
        if await cls.exists(user_id):
            logger.info(f"User {user_id} is already an admin.")
            return 
        # Add an admin to the database
        data = {
            "user_id" : user_id,
            "username" : username,
            "created_at" : datetime.utcnow()
        }
        await cls.user_collection.insert_one(data)
                    
    @classmethod
    async def remove(cls , user_id : int):
        # Remove an admin from the database
        return await cls.user_collection.delete_one({"user_id" : user_id})
    
    @classmethod
    async def exists(cls , user_id : int) -> bool:
        return await cls.user_collection.find_one({"user_id" : user_id} , {"_id" : 0}) is not None
    
    @classmethod
    async def all(cls):
        # Get all admins
        cursor = cls.user_collection.find({} , {"_id" : 0})
        return [doc async for doc in cursor] 

