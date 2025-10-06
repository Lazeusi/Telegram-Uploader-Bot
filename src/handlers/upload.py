from aiogram import Router , types , F
from src.database.models.file import File
from src.database.models.admin import Admin
from aiogram.utils.deep_linking import create_start_link
from src.logger import logger

router = Router()

@router.message(F.content_type.in_({"photo" , "video" , "document"}))
async def upload_handler(message: types.Message , bot):
    
    user_id = message.from_user.id
    if not await Admin.exists(user_id):
        await message.reply("You are not authorized to use this bot.")
        logger.warning(f"Unauthorized access attempt by user: {user_id}")
        return  # Stop further processing if not an admin
    
    if message.photo:
        file_type = "photo"
        file_id = message.photo[-1].file_id
    elif message.video:
        file_type = "video"
        file_id = message.video.file_id
    elif message.document:
        file_type = "document"
        file_id = message.document.file_id
    else:
        await message.reply("Unsupported file type. Please upload a photo, video, or document.")
        return  # Stop further processing if not a photo, video, or document
    
    stored_file_id = await File.add(
        telegram_file_id=file_id,
        file_type=file_type,
        uploaded_by=user_id
    )
    
    
    link = await create_start_link(bot, payload=stored_file_id)
    await message.reply(f"File uploaded successfully! Download link: {link}")