from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton


class CancelKeyboard:
    CANCEL = "Bekor qilish ❌"

    @classmethod
    def get_keyboard(cls) -> ReplyKeyboardMarkup:
        buttons = [
            [KeyboardButton(text=cls.CANCEL)],
        ]

        keyboard = ReplyKeyboardBuilder(markup=buttons)
        return keyboard.as_markup(
            resize_keyboard=True,
        )
