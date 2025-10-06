from aiogram import Router , types ,F
from src.database.models.channel import Channel
from src.keyboards.inline.channel import ch_kb , list_channels


router = Router()

@router.callback_query(F.data == "list_channels")
async def view_channels_callback_handler(callback_query: types.CallbackQuery):
    chan = await Channel.get_all()
    if not chan:
        await callback_query.message.edit_text("No channels found.")
        return
    await callback_query.message.edit_text("Here are the channels you have added:" , reply_markup=await list_channels())

@router.callback_query(F.data == "back_to_main")
async def back_to_main_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("Select an option" , reply_markup=ch_kb)
    await callback_query.answer()  # Acknowledge the callback to remove the loading state