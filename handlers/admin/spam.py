from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from services.logger import log
from filters.is_admin import IsAdmin
from filters.callback_data_filter import *
from states.admin.spam import *

from database.crud import users as crud_users

router = Router()


@log.catch()
@router.callback_query(IsAdmin(), CallbackDataFilter('spam'))
async def spam(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer()
    await call.message.answer('Пришли мне сообщение которое нужно разослать\n\n'
                              '<i>**медиагруппы не поддерживаются</i>')
    await state.set_state(Spam.spam_message)


@log.catch()
@router.message(IsAdmin(), Spam.spam_message)
async def get_spam_message(message: Message, state: FSMContext, db_session: AsyncSession):
    all_users = await crud_users.get_list_all_users(db_session)
    count_all_users = len(all_users)
    await message.answer(f'Считано: {count_all_users} пользователей, запускаю рассылку')
    sended = 0
    for user_id in all_users:
        try:
            await message.copy_to(user_id)
            sended += 1
        except:
            continue
    await message.answer(f'Рассылка окончена\n'
                         f'Отправлено: {sended} пользователям\n'
                         f'{count_all_users-sended} пользователей заблокировало бота')