from aiogram import Dispatcher
from handlers.client.start import router as start_router
from handlers.admin.panel import router as admin_router
from handlers.admin.utm import router as utm_router
from handlers.admin.spam import router as spam_router


def register_handlers(dp: Dispatcher):
    dp.include_routers(start_router)
    dp.include_routers(admin_router)
    dp.include_routers(utm_router)
    dp.include_routers(spam_router)