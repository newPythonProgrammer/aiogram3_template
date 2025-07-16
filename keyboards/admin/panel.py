from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_main_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="🔔 Рассылка", callback_data="mailing")],
        [InlineKeyboardButton(text="🔗 UTM ссылки", callback_data="utm")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
