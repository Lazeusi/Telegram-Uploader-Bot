from .start import router as start_router
from .error_handler import router as error_router
from .admin import router as admin_router
from .upload import router as upload_router
async def setup_routers(dp):
    dp.include_router(error_router)
    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.include_router(upload_router)