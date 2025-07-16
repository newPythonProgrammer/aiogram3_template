from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def utm_main_keyboard(current_page: int, total_pages: int) -> InlineKeyboardMarkup:
    keyboard = []

    nav_buttons = []

    if current_page > 1:
        nav_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"utm_page:{current_page - 1}"))

    nav_buttons.append(InlineKeyboardButton(text=f"{current_page}/{total_pages}", callback_data="noop"))

    if current_page < total_pages:
        nav_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"utm_page:{current_page + 1}"))

    # Добавляем строку навигации
    keyboard.append(nav_buttons)

    # Добавляем остальные кнопки по строкам
    keyboard.append([InlineKeyboardButton(text="🆕 Создать utm", callback_data="create_utm")])
    keyboard.append([InlineKeyboardButton(text="🗑 Удалить utm", callback_data="delete_utm")])
    keyboard.append([InlineKeyboardButton(text="🔙 Главное меню", callback_data="admin_menu")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
