from uuid import uuid4
from src.database.connection import db
from datetime import datetime


class File:
    collection = db.files
    
    @classmethod
    async def add(cls , telegram_file_id : str , file_type : str , uploaded_by: int):
        file_id = str(uuid4())[:8]
        
        data = {
            "file_id" : file_id,
            "telegram_file_id" : telegram_file_id,
            "file_type" : file_type,
            "uploaded_by" : uploaded_by,
            "created_at" : datetime.utcnow()
        }
        
        await cls.collection.insert_one(data)
        return file_id
    
    @classmethod
    async def get(cls , file_id : str):
        return await cls.collection.find_one({"file_id" : file_id})