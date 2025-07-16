from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from config import get_settings

settings = get_settings()


class IsAdmin(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        user_id = event.from_user.id  # работает и для Message, и для CallbackQuery
        return user_id in settings.bot.admins