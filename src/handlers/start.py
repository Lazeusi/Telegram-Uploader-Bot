from aiogram import types , Router
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def start_command_handler(message: types.Message):
    await message.answer(f"Hello {message.from_user.full_name}")