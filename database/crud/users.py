from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User
from typing import Optional
import datetime


async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
    result = await session.execute(select(User).where(User.user_id == user_id))
    return result.scalar_one_or_none()


async def create_user(
        session: AsyncSession,
        user_id: int,
        first_name: str,
        last_name: str,
        utm: Optional[str] = None,
) -> User:
    user = User(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        utm=utm,
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow(),
    )
    session.add(user)
    await session.commit()
    return user


async def update_user_name(
        session: AsyncSession,
        user_id: int,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
) -> None:
    user = await get_user_by_id(session, user_id)
    if user:
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.updated_at = datetime.datetime.utcnow()
        await session.commit()


async def get_user_stat(session: AsyncSession):
    now = datetime.datetime.now()
    today = now.date()
    week_ago = now - datetime.timedelta(days=7)
    month_ago = now - datetime.timedelta(days=30)

    total_stmt = select(func.count()).select_from(User)
    today_stmt = select(func.count()).where(func.date(User.created_at) == today)
    week_stmt = select(func.count()).where(User.created_at >= week_ago)
    month_stmt = select(func.count()).where(User.created_at >= month_ago)

    total = await session.scalar(total_stmt)
    today = await session.scalar(today_stmt)
    week = await session.scalar(week_stmt)
    month = await session.scalar(month_stmt)

    return {
        "total": total or 0,
        "today": today or 0,
        "week": week or 0,
        "month": month or 0
    }


async def get_list_all_users(session: AsyncSession) -> list[int]:
    result = await session.execute(select(User.user_id))
    return result.scalars().all()