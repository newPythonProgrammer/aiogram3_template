from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup
from filters.is_admin import IsAdmin
from filters.callback_data_filter import *
from keyboards.admin.utm import utm_main_keyboard
from database.crud import utm as crud_utm
from states.admin.utm import *
from services.logger import log

router = Router()


def format_utm_block(data: list[list], username: str, page: int, per_page: int = 5) -> tuple[str, InlineKeyboardMarkup]:
    total = len(data)  # Всего ссылок
    total_pages = (total + per_page - 1) // per_page  # Всего страниц будет
    page = max(1, min(page, total_pages))  # Страница текущая номер, не индекс. Ограничиваем
    start = (page - 1) * per_page  # Срезаем
    end = start + per_page
    chunk = data[start:end]

    text = "🔗 <b>UTM ссылки</b>\n\n"
    for utm, created_at, count in chunk:
        text += (
            f"🔗 <code>https://t.me/{username}?start={utm}</code>\n"
            f"📅 Создана: {created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"👥 Пользователей: {count}\n\n"
        )

    keyboard = utm_main_keyboard(page, total_pages)
    return text, keyboard


@log.catch()
@router.callback_query(IsAdmin(), CallbackDataFilter('utm'))
async def utm_menu(call: CallbackQuery, db_session: AsyncSession):
    await call.answer()
    bot_info = await call.bot.get_me()
    all_utm = await crud_utm.get_all_utm(db_session)

    text, keyboard = format_utm_block(all_utm, bot_info.username, 1)

    await call.message.answer(f'<b>UTM ссылки</b>\n\n'
                              f'В этом разделе вы можете создавать уникальные пригласительные ссылки, по которым '
                              f'сможете отслеживать сколько пришло новых пользователей по ссылке.\n\n'
                              f'{text}',
                              reply_markup=keyboard)


@log.catch()
@router.callback_query(IsAdmin(), CallbackDataFilter('create_utm'))
async def create_utm(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer()
    await state.set_state(CreateUTM.utm)
    bot_info = await call.bot.get_me()
    await call.message.answer('Введите метку.\n\n'
                              f'Она будет в ссылки ввида <code>https://t.me/{bot_info.username}?start=utm</code> вместо utm')


@log.catch()
@router.message(IsAdmin(),
                CreateUTM.utm)
async def get_utm_for_create(message: Message, state: FSMContext, db_session: AsyncSession):
    message_text = message.text
    bad_char = ['&', '!', '@', '#', '$', '^', '*', '(', ')', '-']
    if any(word in message_text for word in bad_char):
        await message.answer('В utm не должно быть спец. символов')
        return
    if len(message_text.split()) > 1:
        await message.answer('Введите одно слово')
        return

    await crud_utm.create_utm(db_session, message_text)
    bot_info = await message.bot.get_me()
    await message.answer('UTM добавлена\n\n'
                         f'<code>https://t.me/{bot_info.username}?start={message_text}</code>')

    all_utm = await crud_utm.get_all_utm(db_session)

    text, keyboard = format_utm_block(all_utm, bot_info.username, 1)
    await message.answer(f'<b>UTM ссылки</b>\n\n'
                         f'В этом разделе вы можете создавать уникальные пригласительные ссылки, по которым '
                         f'сможете отслеживать сколько пришло новых пользователей по ссылке.\n\n'
                         f'{text}',
                         reply_markup=keyboard)
    await state.clear()


@log.catch()
@router.callback_query(IsAdmin(), CallbackDataFilterPrefix('utm_page'))
async def leaf_page(call: CallbackQuery, state: FSMContext, db_session: AsyncSession):
    await state.clear()
    await call.answer()
    page = int(call.data.split(':')[-1])
    all_utm = await crud_utm.get_all_utm(db_session)
    bot_info = await call.bot.get_me()
    text, keyboard = format_utm_block(all_utm, bot_info.username, page)
    await call.message.edit_text(
        text=(
            f'<b>UTM ссылки</b>\n\n'
            f'В этом разделе вы можете создавать уникальные пригласительные ссылки, по которым '
            f'сможете отслеживать сколько пришло новых пользователей по ссылке.\n\n'
            f'{text}'
        ),
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@log.catch()
@router.callback_query(IsAdmin(), CallbackDataFilter('delete_utm'))
async def delete_utm(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer('Пришлите ссылку которую хотите удалить')
    await state.set_state(DeleteUTM.link)


@log.catch()
@router.message(IsAdmin(), DeleteUTM.link)
async def get_link_for_delete(message: Message, state: FSMContext, db_session: AsyncSession):
    utm = message.text.split("=")[-1] if len(message.text.split('=')) > 1 else None
    if not utm:
        await message.answer('Ссылка не найдена')
        await state.clear()
        return

    is_deleted = await crud_utm.delete_utm(db_session, utm)

    if is_deleted:
        await message.answer('Ссылка удалена')
    else:
        await message.answer('Ссылка не найдена')
    await state.clear()