from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ch_kb = InlineKeyboardMarkup(inline_keyboard= [
    [InlineKeyboardButton(text="Add Channel", callback_data="add_channel") , InlineKeyboardButton(text="Remove Channel", callback_data="remove_channel")],
    [InlineKeyboardButton(text="List Channels", callback_data="list_channels")] 
] ) 
