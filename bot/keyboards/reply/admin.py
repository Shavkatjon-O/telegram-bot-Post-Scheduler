from aiogram.types import ReplyKeyboardMarkup, KeyboardButtonRequestUser
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton


class AdminMenuKeyboard:
    CREATE = "Qo'shish 📝"
    DELETE = "O'chirish 🗑"
    MENU = "Asosiy menu 🏠"

    @classmethod
    def get_keyboard(cls) -> ReplyKeyboardMarkup:
        buttons = [
            [KeyboardButton(text=cls.CREATE)],
            [KeyboardButton(text=cls.DELETE)],
            [KeyboardButton(text=cls.MENU)],
        ]
        keyboard = ReplyKeyboardBuilder(markup=buttons)
        keyboard.adjust(2, 1)

        return keyboard.as_markup(resize_keyboard=True)


def get_create_admin_keyboard() -> ReplyKeyboardMarkup:
    button = KeyboardButton(
        text="Admin tanlash 🧑‍💼",
        request_user=KeyboardButtonRequestUser(request_id=1, user_is_bot=False),
    )
    markup = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
    return markup
