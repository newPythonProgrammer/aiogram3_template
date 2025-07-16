from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class CallbackDataFilter(BaseFilter):
    def __init__(self, data: str):
        self.data = data

    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data and callback.data == self.data

class CallbackDataFilterPrefix(BaseFilter):
    def __init__(self, prefix: str):
        self.prefix = prefix

    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data and callback.data.startswith(self.prefix)
