from .start import router as start_router
from .error_handler import router as error_router
from .admin import router as admin_router
from .upload import router as upload_router
from .channel import router as channel_router
from .add_channel import router as add_channel_router
from .rem_channel import router as rem_channel_router
from .view_channel import router as view_channel_router

async def setup_routers(dp):
    dp.include_router(error_router)
    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.include_router(upload_router)
    dp.include_router(channel_router)
    dp.include_router(rem_channel_router)
    dp.include_router(view_channel_router)
    dp.include_router(add_channel_router)