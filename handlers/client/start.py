from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Router, types
from aiogram.filters import CommandStart
from services.logger import log

from database.crud import users as crud_users

router = Router()


@log.catch()
@router.message(CommandStart())
async def start_handler(message: types.Message, db_session: AsyncSession):
    utm = message.text.split()[-1] if len(message.text.split())>1 else None
    user = await crud_users.get_user_by_id(db_session, message.from_user.id)

    if not user:
        await crud_users.create_user(
            db_session,
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            utm=utm
        )
    else:
        await crud_users.update_user_name(
            db_session,
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
    await message.answer('Привет')
