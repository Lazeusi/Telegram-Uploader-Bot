from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from src.database.models.channel import Channel

ch_kb = InlineKeyboardMarkup(inline_keyboard= [
    [InlineKeyboardButton(text="Add Channel", callback_data="add_channel") , InlineKeyboardButton(text="Remove Channel", callback_data="remove_channel")],
    [InlineKeyboardButton(text="List Channels", callback_data="list_channels")] 
] ) 

cancel_add_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Cancel", callback_data="cancel_add")]
    ])
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def channels_inline_keyboard():
    channels = await Channel.get_all()

    # ساخت ردیف‌های دکمه‌های چنل
    buttons = [
        [InlineKeyboardButton(
            text=channel.get("title", "No Title"),
            callback_data=f"channel_{channel['channel_id']}"
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

async def list_channels():
    channels = await Channel.get_all()

    buttons = [
        [InlineKeyboardButton(
            text=channel.get("title", "No Title"),
            callback_data=f"channel_{channel['channel_id']}"
        )] 
        for channel in channels
    ]


    buttons.append([InlineKeyboardButton(text="🔙 Back", callback_data="back_to_main")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
