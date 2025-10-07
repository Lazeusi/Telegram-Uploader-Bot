from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from src.database.models.channel import Channel

ch_kb = InlineKeyboardMarkup(inline_keyboard= [
    [InlineKeyboardButton(text="Add Channel", callback_data="add_channel") , InlineKeyboardButton(text="Remove Channel", callback_data="remove_channel")],
    [InlineKeyboardButton(text="List Channels", callback_data="list_channels")] 
] ) 

cancel_add_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Cancel", callback_data="cancel_add")]
    ])


async def channels_inline_keyboard():
    channels = await Channel.get_all()

    # ساخت ردیف‌های دکمه‌های چنل
    buttons = [
        [InlineKeyboardButton(
            text=channel.get("title"),
            callback_data=f"channel_{channel['identifier']}"
        )] 
        for channel in channels
    ]

    # دکمه برگشت همیشه یک ردیف جداگانه
    
    buttons.append([InlineKeyboardButton(text="🔙 Back", callback_data="back_to_main")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard



accept_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Yes, Delete", callback_data="confirm_delete"), InlineKeyboardButton(text="Cancel", callback_data="cancel_delete")]
    ])



from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.database.models.channel import Channel


async def list_channels(bot):
    channels = await Channel.get_all()
    buttons = []

    for ch in channels:
        chat_id = int(ch["identifier"])

        try:
            chat = await bot.get_chat(chat_id)
            title = chat.title or str(chat_id)

            # if chat has a username, use it to create a t.me link
            if chat.username:
                url = f"https://t.me/{chat.username}"
            else:
                # if chat has an invite link, use it
                if chat.invite_link:
                    url = chat.invite_link
                else:
                    # otherwise, create a link using the chat ID (only works for supergroups and channels)
                    url = f"https://t.me/c/{str(chat_id)[4:]}" if str(chat_id).startswith("-100") else None

        except Exception as e:
            print(f"⚠️ Failed to fetch chat info for {chat_id}: {e}")
            title = f"Unknown Chat ({chat_id})"
            url = None

        if url:
            buttons.append([InlineKeyboardButton(text=title, url=url)])

    buttons.append([InlineKeyboardButton(text="🔙 Back", callback_data="back_to_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)




    
