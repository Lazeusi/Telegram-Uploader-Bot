from aiogram import Router , types ,F
from src.database.models.channel import Channel

router = Router()

@router.callback_query(F.data == "remove_channel")
async def remove_channel_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Please send the channel username or ID to remove it.")
    await callback_query.answer()  # Acknowledge the callback to remove the loading state