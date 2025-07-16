from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from filters.is_admin import IsAdmin
from filters.callback_data_filter import CallbackDataFilter
from keyboards.admin.panel import admin_main_keyboard
from services.logger import log
from database.crud import users as crud_users

router = Router()


@log.catch()
@router.message(IsAdmin(), Command('panel'))
async def admin_panel(message: Message, state: FSMContext, db_session: AsyncSession):
    await state.clear()
    statistic = await crud_users.get_user_stat(db_session)
    await message.answer("Добро пожаловать в админку!\n\n"
                         "📈 Динамика:\n"
                         f"├ За день: {statistic['today']}\n"
                         f"├ За неделю: {statistic['week']}\n"
                         f"├ За месяц: {statistic['month']}\n"
                         f"└ Всего: {statistic['total']}", reply_markup=admin_main_keyboard())


@log.catch()
@router.callback_query(IsAdmin(), CallbackDataFilter('admin_menu'))
async def admin_panel(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    await call.message.edit_text("Добро пожаловать в админку!", reply_markup=admin_main_keyboard())