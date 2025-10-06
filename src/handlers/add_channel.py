from src.keyboards.inline.channel import ch_kb
from aiogram import Router , types , F , Bot
from aiogram.fsm.state import StatesGroup , State
from aiogram.fsm.context import FSMContext
from src.database.models.channel import Channel
from src.logger import logger


router = Router()


class AddChannelState(StatesGroup):
    waiting_for_channel = State()
    
@router.callback_query(F.data == "add_channel")
async def add_channel_callback_handler(callback_query: types.CallbackQuery , state: FSMContext):
    await callback_query.message.answer("Please send the channel username or ID to add it.")
    await state.set_state(AddChannelState.waiting_for_channel)
    await callback_query.answer()  # Acknowledge the callback to remove the loading state
    
@router.message(AddChannelState.waiting_for_channel)
async def process_channel_input(message: types.Message , state: FSMContext , **kwargs):
    bot= kwargs["bot"]
    identifier = message.text.strip().lower()
    
    try:
        chat = await bot.get_chat(identifier)
        if chat.type not in ["channel", "supergroup"]:
            await message.reply("The provided ID/username does not belong to a channel or supergroup. Please try again.")
            return
        await Channel.add(
            channel_id=chat.id,
            title=chat.title,
            channel_username=chat.username
        )
        await message.reply(f"Channel '{chat.title}' has been added successfully.")
    except Exception as e:
        await message.reply("Failed to add the channel. Please ensure the bot is an admin in the channel and the ID/username is correct.")
        logger.error(f"Failed to add channel: {e} \n Channel ID: {identifier} \n User ID: {message.from_user.id}" , exc_info=True)
        
        