# middlewares/db.py
from database.session import get_db_session


class DBSessionMiddleware:
    def __init__(self):
        pass  # если нужно, можно передавать session factory

    async def __call__(self, handler, event, data):
        async with get_db_session() as db:
            data["db_session"] = db  # передаём в хендлер через kwargs
            return await handler(event, data)
