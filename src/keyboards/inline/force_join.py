from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def generate_join_keyboard(chats: list):
    """
    Create inline keyboard with join buttons for all required chats,
    plus a 'Joined' button at the end.
    """
    buttons = []

    for chat in chats:
        identifier = chat["identifier"]
        title = chat.get("title", str(identifier))

        # Construct URL
        if str(identifier).startswith("-100"):
            # Private supergroup/channel
            url = f"https://t.me/c/{str(identifier)[4:]}"
        else:
            url = f"https://t.me/{identifier}"  # fallback

        buttons.append([InlineKeyboardButton(text=title, url=url)])

    # Add final "Joined" button
    buttons.append([InlineKeyboardButton(text="✅ Joined", callback_data="join")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
