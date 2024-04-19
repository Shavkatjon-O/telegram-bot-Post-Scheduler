from aiogram.fsm.state import State, StatesGroup


class StartStates(StatesGroup):
    START = State()


class AdminStates(StatesGroup):
    ADMIN = State()
    CREATE = State()
    DELETE = State()


class ChatStates(StatesGroup):
    CHAT = State()
    CREATE = State()
    DELETE = State()
