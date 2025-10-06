from aiogram import Router , types ,F
from src.database.models.channel import Channel
from src.keyboards.inline.channel import ch_kb


router = Router()

@router.callback_query(F.data == "view_channels")
async def view_channels_callback_handler(callback_query: types.CallbackQuery):
    pass
