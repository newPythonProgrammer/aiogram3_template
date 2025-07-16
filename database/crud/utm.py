from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import UTM, User
from typing import Optional
import datetime


async def create_utm(session: AsyncSession, utm: str) -> UTM:
    utm_model = UTM(utm=utm)
    session.add(utm_model)
    await session.commit()
    return utm_model


async def get_all_utm(session: AsyncSession) -> list[list]:
    result = await session.execute(
        select(
            UTM.utm,
            UTM.created_at,
            func.count(User.user_id).label("user_count")
        ).outerjoin(User, User.utm == UTM.utm)
        .group_by(UTM.utm, UTM.created_at)
        .order_by(UTM.created_at.desc())
    )
    return [[utm, created_at, count] for utm, created_at, count in result.all()]


async def delete_utm(session: AsyncSession, utm: str):
    result = await session.execute(delete(UTM).where(UTM.utm == utm))
    await session.commit()
    return result.rowcount > 0
