from aiogram.fsm.state import State, StatesGroup


class ManageStates(StatesGroup):
    MANAGE = State()


class AdminStates(StatesGroup):
    ADMIN = State()
    CREATE_OR_DELETE = State()
