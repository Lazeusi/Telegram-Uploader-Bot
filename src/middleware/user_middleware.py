from aiogram import BaseMiddleware
from aiogram.types import Message
from src.database.models.user import User


class UserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event : Message, data : dict):
        user_id = event.from_user.id
        user_data = {
            "user_id" : user_id ,
            "first_name" : event.from_user.first_name,
            "username" : event.from_user.username or None,
        }
        
        exists = await User.exists(user_id)
        if not exists:
            await User.create(user_data)
            print(f"New user created: {user_id}")
        else:
            await User.update(user_id , user_data)
            print(f"User updated: {user_id}")
            
        return await handler(event, data)