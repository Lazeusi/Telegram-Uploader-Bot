from aiogram import Router , types
from aiogram.filters import Command
import asyncio
from src.database.models.admin import Admin
from src.database.models.user import User
from src.logger import logger

router = Router()

@router.message(Command("add_admin"))
async def add_admin_handler(message: types.Message):
    # Check if the user is an admin
    check_admin = await Admin.exists(message.from_user.id)
    if not check_admin:
        return await message.reply("❌ You are not authorized to use this command.")
    
    args = message.text.split()
    if len(args) != 2:
        return await message.reply("Usage: /add_admin <user_id> or <username>")
    
    identifier = args[1]

    user_id = None
    username = None

    # If the identifier starts with '@', it's a username
    if identifier.startswith("@"):
        username = identifier[1:]
        user_doc = await User.collection.find_one({"username": username.lower()})
        if not user_doc:
            return await message.reply(f"❌ User @{username} not found in users collection.")
        user_id = user_doc["user_id"]

    # If it's a numeric ID
    else:
        try:
            user_id = int(identifier)
            # Check if the user exists in the users collection
            user_doc = await User.collection.find_one({"user_id": user_id})
            if user_doc:
                username = user_doc.get("username")
        except ValueError:
            return await message.reply("⚠️ Invalid user ID.")

    if not user_id:
        return await message.reply("❌ User not found.")
    
    if await Admin.exists(user_id):
        return await message.reply(f"⚠️ User {user_id} is already an admin.")
    # Aded admin
    await Admin.add(user_id, username)
      # Give some time for the database to update
    await asyncio.sleep(3)
    if await Admin.exists(user_id):
        await message.reply(f"✅ User {user_id} has been added as an admin.")
        logger.info(f"Admin added: {user_id} by {message.from_user.id}")
    else:
        await message.reply("❌ Failed to add admin. Please try again later.")
        logger.error(f"Failed to add admin: {user_id} by {message.from_user.id} - From handlers/admin.py - add_admin_handler")
    