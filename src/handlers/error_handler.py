from aiogram import Router , types
from aiogram.types import ErrorEvent
from src.logger import logger

router = Router()

@router.errors()
async def global_error_handler(event: ErrorEvent):
    err = event.exception
    logger.error(f"An error occurred: {err}" , exc_info=True)

    try:
        if isinstance(event.update, types.Message):
            await event.update.reply("An unexpected error occurred. Please try again later.")
    except Exception as e:
        logger.error(f"Failed to send error message to user: {e}", exc_info=True)