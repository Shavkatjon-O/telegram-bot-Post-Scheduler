from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton


class AdminKeyboards:
    CREATE = "Создать ➕"
    DELETE = "Удалить ➖"
    MENU = "Главное меню 🏠"

    @classmethod
    def get_keyboard(cls) -> ReplyKeyboardMarkup:
        buttons = [
            [KeyboardButton(text=cls.CREATE)],
            [KeyboardButton(text=cls.DELETE)],
            [KeyboardButton(text=cls.MENU)],
        ]

        keyboard = ReplyKeyboardBuilder(markup=buttons)
        keyboard.adjust(2, 1)
        keyboard = keyboard.as_markup(resize_keyboard=True)
        return keyboard


class CancelKeyboard:
    CANCEL = "Отмена ❌"

    @classmethod
    def get_keyboard(cls) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=cls.CANCEL)],
            ],
            resize_keyboard=True,
        )
