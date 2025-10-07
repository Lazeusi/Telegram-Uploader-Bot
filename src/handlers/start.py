# src/routers/start_router.py
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from src.database.models.file import File
from src.database.models.channel import Channel
from src.keyboards.inline.force_join import generate_join_keyboard
from src.logger import logger

router = Router()


async def check_join(bot, user_id):
    """
    Check if user has joined all required channels.
    Returns: (joined: bool, keyboard: InlineKeyboardMarkup | None)
    """
    required_chats = await Channel.get_all()
    not_joined = []

    for chat in required_chats:
        chat_id = int(chat["identifier"])
        try:
            member = await bot.get_chat_member(chat_id, user_id)
            if member.status in ("left", "kicked"):
                not_joined.append(chat)
        except Exception:
            not_joined.append(chat)

    if not_joined:
        keyboard = await generate_join_keyboard(not_joined)
        return False, keyboard
    return True, None


@router.message(CommandStart(deep_link=True))
async def start_command_handler(message: types.Message, command: CommandStart, bot, state: FSMContext):
    """
    Handle /start with deep_link (file payload), check join, and send file if allowed.
    """
    file_id = command.args
    await state.update_data(file_id=file_id)  # save payload

    # --- Check join ---
    joined, keyboard = await check_join(bot, message.from_user.id)
    if not joined:
        await message.answer(
            "⚠️ You need to join required channels/groups first:",
            reply_markup=keyboard
        )
        return  # Stop handler until user joins

    # --- Continue handler if joined ---
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
            await bot.send_photo(chat_id=message.chat.id, photo=telegram_file_id)
        elif file_type == "video":
            await bot.send_video(chat_id=message.chat.id, video=telegram_file_id)
        elif file_type == "document":
            await bot.send_document(chat_id=message.chat.id, document=telegram_file_id)
        else:
            await message.reply("Unsupported file type.")
            return
        await message.answer("Here is your file! Bot created by @Lazeusi")
    except Exception as e:
        await message.reply(
            "Failed to retrieve the file. It might have been deleted.",
            parse_mode="Markdown"
        )
        logger.error(
            f"Failed to retrieve the file: {e}\nFile ID: {file_id}\nUser ID: {message.from_user.id}\n"
            f"File Type: {file_type}\nTelegram File ID: {telegram_file_id}",
            exc_info=True
        )


# --- Callback for Joined button ---
@router.callback_query(lambda c: c.data == "join")
async def joined_callback(callback: types.CallbackQuery, state: FSMContext, bot):
    user_id = callback.from_user.id

    joined, keyboard = await check_join(bot, user_id)
    if not joined:
        await callback.answer("❌ You still haven't joined all required channels.")
        return

    await callback.answer("✅ You have joined all channels! Continuing...")
    await callback.message.delete()

    # Retrieve saved payload and trigger file sending
    data = await state.get_data()
    file_id = data.get("file_id")
    if not file_id:
        await bot.send_message(chat_id=user_id, text="Error: No payload found.")
        return

    file_doc = await File.get(file_id)
    if not file_doc:
        await bot.send_message(chat_id=user_id, text="Invalid or expired link.")
        return

    file_type = file_doc["file_type"]
    telegram_file_id = file_doc["telegram_file_id"]

    try:
        if file_type == "photo":
            await bot.send_photo(chat_id=user_id, photo=telegram_file_id)
        elif file_type == "video":
            await bot.send_video(chat_id=user_id, video=telegram_file_id)
        elif file_type == "document":
            await bot.send_document(chat_id=user_id, document=telegram_file_id)
        await bot.send_message(chat_id=user_id, text="Here is your file! Bot created by @Lazeusi")
    except Exception as e:
        await bot.send_message(chat_id=user_id, text="Failed to retrieve the file. It might have been deleted.")
        logger.error(f"Failed to send file: {e}", exc_info=True)
