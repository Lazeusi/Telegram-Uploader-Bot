from aiogram import Router , types ,F
from src.database.models.channel import Channel
from src.keyboards.inline.channel import channels_inline_keyboard , accept_kb , ch_kb
from aiogram.fsm.state import StatesGroup , State
from aiogram.fsm.context import FSMContext
router = Router()

@router.callback_query(F.data == "remove_channel")
async def remove_channel_callback_handler(callback: types.CallbackQuery):
    channels = await Channel.get_all()
    
    if not channels:
        await callback.message.edit_text("No channels found.")
        return
    
    
    await callback.message.edit_text("Please select the channel you want to delete." , reply_markup=await channels_inline_keyboard())
    

class RemoveChannelState(StatesGroup):
    waiting_for_confirmation = State()
    
@router.callback_query(F.data == "back_to_main")
async def back_to_main_callback_handler(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("Select an option" , reply_markup=ch_kb)
    await callback_query.answer()  # Acknowledge the callback to remove the loading state

@router.callback_query(F.data.startswith("channel_"))
async def delete_channel_callback_handler(callback: types.CallbackQuery , state: FSMContext):
    channel_id = str(callback.data.split("_")[1])
    await state.update_data(identifier=channel_id)
    await state.set_state(RemoveChannelState.waiting_for_confirmation)
    await callback.message.edit_text("Are you sure you want to delete this channel?" , reply_markup= accept_kb)
    await callback.answer()  # Acknowledge the callback to remove the loading state
    
@router.callback_query(F.data == "confirm_delete", RemoveChannelState.waiting_for_confirmation)
async def confirm_delete_callback_handler(callback: types.CallbackQuery , state: FSMContext):
    data = await state.get_data()
    channel_id = data.get("identifier")
    if channel_id:
        await Channel.delete(channel_id)
        await callback.message.edit_text("Channel has been removed successfully.")
    else:
        await callback.message.edit_text("No channel selected for deletion.")
    await state.clear()
    await callback.answer()  # Acknowledge the callback to remove the loading state
    
@router.callback_query(F.data == "cancel_delete", RemoveChannelState.waiting_for_confirmation)
async def cancel_delete_callback_handler(callback: types.CallbackQuery , state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Channel deletion has been cancelled.")
    await callback.answer()  # Acknowledge the callback to remove the loading state