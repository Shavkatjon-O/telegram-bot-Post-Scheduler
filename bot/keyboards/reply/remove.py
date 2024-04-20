from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton


class ConfirmKeyboard:
    CONFIRM = "Tasdiqlash ✅"
    CANCEL = "Bekor qilish ❌"

    @classmethod
    def get_keyboard(cls) -> ReplyKeyboardMarkup:
        buttons = [
            [KeyboardButton(text=cls.CONFIRM)],
            [KeyboardButton(text=cls.CANCEL)],
        ]

        keyboard = ReplyKeyboardBuilder(markup=buttons)
        keyboard.adjust(2)

        return keyboard.as_markup(
            resize_keyboard=True,
        )
