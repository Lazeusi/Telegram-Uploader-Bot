from aiogram import BaseMiddleware
from aiogram.types import Message

from src.logger import logger
from src.database.models.user import User



class UserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event : Message, data : dict):
        user_id = event.from_user.id
        username = event.from_user.username
        user_data = {
            "user_id" : user_id ,
            "first_name" : event.from_user.first_name,
            "username" : username.lower() or None,
        }
        
        exists = await User.exists(user_id)
        if not exists:
            await User.create(user_data)
            # logger.warning("Somthing went wrong! | We cant find user or create new one! - (exists Variable) in user_middleware.py")
            logger.info(f"New user joined: {user_id} , Username: {event.from_user.username}")
        else:
            await User.update(user_id , user_data)
            # logger.warning("Somthing went wrong! | We can't update user data! - (exists Variable) in user_middleware.py")
            logger.info(f"User data updated: {user_id} , Username: {event.from_user.username}")
            
        return await handler(event, data)