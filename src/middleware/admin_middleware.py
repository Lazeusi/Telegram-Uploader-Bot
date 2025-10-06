from aiogram import BaseMiddleware
from aiogram.types import Message
from src.database.models.admin import Admin
from src.logger import logger

class AdminMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.from_user.id
        if not await Admin.exists(user_id):
            await event.reply("You are not authorized to use this bot.")
            logger.warning(f"Unauthorized access attempt by user: {user_id}")
            return  # Stop further processing if not an admin
        return await handler(event, data)
        