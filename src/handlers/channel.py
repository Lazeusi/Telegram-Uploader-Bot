from aiogram import Router , types
from aiogram.filters import Command
from src.database.models.channel import Channel
from src.database.models.admin import Admin
from src.logger import logger
from src.keyboards.inline.channel import ch_kb
router = Router()

@router.message(Command("channel"))
async def channel_command_handler(message: types.Message , bot):
    admin = await Admin.exists(message.from_user.id)
    if not admin:
        await message.reply("You are not an admin. Only admins can add channels.")
        return
    await message.reply("Select an option" , reply_markup=ch_kb)