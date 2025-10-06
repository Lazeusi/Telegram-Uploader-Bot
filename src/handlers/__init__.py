from .start import router as start_router

async def setup_routers(dp):
    dp.include_router(start_router)