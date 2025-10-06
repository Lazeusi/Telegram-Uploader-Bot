from .user_middleware import UserMiddleware

async def setup_middlewares(dp):
    dp.message.middleware(UserMiddleware())