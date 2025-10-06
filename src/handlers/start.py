from aiogram import types , Router
from aiogram.filters import CommandStart
from src.database.models.file import File
from src.logger import logger
router = Router()


@router.message(CommandStart(deep_link=True))
async def start_command_handler(message: types.Message , command : CommandStart , bot):
    file_id = command.args
    if not file_id:
        await message.reply("Welcome! Use this bot to upload and share files.")
        return
    file_doc = await File.get(file_id)
    if not file_doc:
        await message.reply("Invalid or expired link.")
        return
    file_type = file_doc["file_type"]
    telegram_file_id = file_doc["telegram_file_id"]
    
    try:
        if file_type == "photo":
            await bot.send_photo(chat_id = message.chat.id , photo = telegram_file_id)
        elif file_type == "video":
            await bot.send_video(chat_id = message.chat.id , video = telegram_file_id)
        elif file_type == "document":
            await bot.send_document(chat_id = message.chat.id , document = telegram_file_id)
        else:
            await message.reply("Unsupported file type.")
            return
        await message.answer("Here is your file! , Bot Created by @Lazeusi")
    except Exception as e:
        await message.reply("Failed to retrieve the file. It might have been deleted." , parse_mode="Markdown")
        logger.error(f"Failed to retrieve the file: {e} \n File ID: {file_id} \n User ID: {message.from_user.id} \n File Type: {file_type} \n Telegram File ID: {telegram_file_id}" , exc_info=True)
        return
            