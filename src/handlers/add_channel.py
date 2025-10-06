from aiogram import Router, types, F, Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from src.keyboards.inline.channel import ch_kb, cancel_add_kb
from src.database.models.channel import Channel
from src.logger import logger
import re

router = Router()


class AddChannelState(StatesGroup):
    waiting_for_channel = State()
    waiting_for_title = State()


@router.callback_query(F.data == "add_channel")
async def add_channel_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(
        "Please send the channel or group username, ID, or invite link.",
        reply_markup=cancel_add_kb
    )
    await state.set_state(AddChannelState.waiting_for_channel)
    await callback_query.answer()


@router.callback_query(F.data == "cancel_add", AddChannelState.waiting_for_channel)
async def cancel_add_callback_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Channel or group addition has been cancelled.")


@router.message(AddChannelState.waiting_for_channel)
async def process_channel_input(message: types.Message, state: FSMContext):
    identifier = message.text.strip()
    
    
    if identifier.startswith("@"):
        chat_type = "public"
    elif "t.me" in identifier:
        chat_type = "invite link"
    elif identifier.lstrip("-").isdigit():
        chat_type = "id"
    else:
        chat_type = "unknown"

    await state.set_data({"identifier": identifier, "chat_type": chat_type})
    
    await state.set_state(AddChannelState.waiting_for_title)
    await message.reply("Please provide a title for the channel or group.")
    

@router.message(AddChannelState.waiting_for_title)
async def process_title_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    identifier = data["identifier"]
    chat_type = data["chat_type"]
    
    title = message.text.strip()
    
    await Channel.add(identifier, title, chat_type)
    await state.clear()
    await message.reply("Channel or group has been added successfully.")