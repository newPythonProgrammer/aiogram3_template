from aiogram.fsm.state import State, StatesGroup


class Spam(StatesGroup):
    spam_message = State()