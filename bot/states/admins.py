from aiogram.fsm.state import State, StatesGroup


class StartStates(StatesGroup):
    START = State()


class AdminStates(StatesGroup):
    ADMIN = State()
    CREATE_OR_DELETE = State()
