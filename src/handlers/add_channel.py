
from aiogram import Router, types, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from src.database.models.channel import Channel
from src.keyboards.inline.channel import cancel_add_kb
import re

router = Router()

class AddChatState(StatesGroup):
    waiting_for_identifier = State()
    waiting_for_forward = State()


@router.callback_query(F.data == "add_channel")
async def start_add_chat(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Send the chat username, ID, or invite link to add it 👇" ,
        reply_markup=cancel_add_kb
    )
    await state.set_state(AddChatState.waiting_for_identifier)
    await callback.answer()


@router.callback_query(F.data == "cancel_add")
async def cancel_add_chat(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Chat addition cancelled.")
    await callback.answer()


@router.message(AddChatState.waiting_for_identifier)
async def process_chat_identifier(message: types.Message, state: FSMContext):
    identifier = message.text.strip()
    bot = message.bot

    # Public chat by username
    if identifier.startswith("@"):
        try:
            chat = await bot.get_chat(identifier)
            await Channel.add(identifier=chat.id, chat_type="public", title=chat.title)
            await message.reply(f"✅ Chat added successfully:\n<b>Title:</b> {chat.title}\n<b>ID:</b> <code>{chat.id}</code>", parse_mode="HTML")
            await state.clear()
        except Exception:
            await message.reply("❌ Failed to add public chat. Make sure the bot is admin and the username is correct.")
    
    # Private invite link
    elif "t.me/+" in identifier or "joinchat" in identifier:
        await state.update_data(pending_identifier=identifier)
        await message.reply("⚠️ For private channels/groups, please forward a post from that chat so we can get the real ID.")
        await state.set_state(AddChatState.waiting_for_forward)
    
    # Numeric ID
    elif identifier.lstrip("-").isdigit():
        chat_id = int(identifier)
        try:
            chat = await bot.get_chat(chat_id)
            await Channel.add(identifier=chat.id, chat_type="id", title=chat.title)
            await message.reply(f"✅ Chat added successfully:\n<b>Title:</b> {chat.title}\n<b>ID:</b> <code>{chat.id}</code>", parse_mode="HTML")
            await state.clear()
        except Exception:
            await message.reply("❌ Failed to add chat with ID. Make sure the bot is admin in the chat.")
    else:
        await message.reply("❌ Invalid input. Please send username, numeric ID, or invite link.")


@router.message(AddChatState.waiting_for_forward)
async def process_forwarded_chat(message: types.Message, state: FSMContext):
    if not message.forward_from_chat:
        await message.reply("❌ No forwarded message detected. Please forward a post from the private chat.")
        return

    chat = message.forward_from_chat
    await Channel.add(identifier=chat.id, chat_type="private", title=chat.title)
    await message.reply(f"✅ Private chat added successfully:\n<b>Title:</b> {chat.title}\n<b>ID:</b> <code>{chat.id}</code>", parse_mode="HTML")
    await state.clear()
