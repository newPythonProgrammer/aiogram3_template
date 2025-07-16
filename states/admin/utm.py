from aiogram.fsm.state import State, StatesGroup


class CreateUTM(StatesGroup):
    utm = State()

class DeleteUTM(StatesGroup):
    link = State()