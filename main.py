from aiogram import Bot, Dispatcher
import asyncio
import logging

from src.config import settings
from src.database.connection import db
from src.handlers import setup_routers
from src.middleware import setup_middlewares


async def main():
    
    await db.test_connection()
    
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    
    await setup_routers(dp)
    await setup_middlewares(dp)
    


    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)
    print("Bot started!🚀")
    
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped!💕")