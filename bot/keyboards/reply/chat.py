from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton


class ChatKeyboard:
    """Keyboards for chat handlers."""

    CREATE = "Qo'shish ➕"
    DELETE = "O'chirish ➖"
    MENU = "Asosiy menyu 🏠"

    @classmethod
    def get_keyboard(cls) -> ReplyKeyboardMarkup:
        """Get chat keyboard."""
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
