from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton


class AdminKeyboards:
    CREATE = "Yaratish ➕"
    DELETE = "O'chirish ➖"
    MENU = "Asosiy menyu 🏠"

    @classmethod
    def get_keyboard(cls) -> ReplyKeyboardMarkup:
        buttons = [
            [KeyboardButton(text=cls.CREATE)],
            [KeyboardButton(text=cls.DELETE)],
            [KeyboardButton(text=cls.MENU)],
        ]

        keyboard = ReplyKeyboardBuilder(markup=buttons)
        keyboard.adjust(2, 1)
        return keyboard.as_markup(
            resize_keyboard=True,
        )


class CancelKeyboard:
    CANCEL = "Bekor qilish ❌"

    @classmethod
    def get_keyboard(cls) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=cls.CANCEL)],
            ],
            resize_keyboard=True,
        )
