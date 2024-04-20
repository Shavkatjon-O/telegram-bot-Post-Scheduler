from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton


class StartKeyboard:
    CHATS = "Chatlar 📝"
    CREATE_POST = "Post yaratish 📢"
    ADMINS = "Adminlar 👤"
    HELP = "Yordam 🆘"
    REMOVE_ALL_POSTS = "Barcha postlarni o'chirish 🗑"

    @classmethod
    def get_keyboard(cls) -> ReplyKeyboardMarkup:
        buttons = [
            [KeyboardButton(text=cls.CREATE_POST)],
            [KeyboardButton(text=cls.CHATS)],
            [KeyboardButton(text=cls.HELP)],
            [KeyboardButton(text=cls.ADMINS)],
            [KeyboardButton(text=cls.REMOVE_ALL_POSTS)],
        ]

        keyboard = ReplyKeyboardBuilder(markup=buttons)
        keyboard.adjust(1, 3, 1)
        return keyboard.as_markup(
            resize_keyboard=True,
        )


def get_buttons():
    from bot.handlers.admin import command_admin_handler
    from bot.handlers.chat import command_chat_handler
    from bot.handlers.post import command_post_handler
    from bot.handlers.help import command_help_handler
    from bot.handlers.remove import command_remove_handler

    return {
        StartKeyboard.CREATE_POST: command_post_handler,
        StartKeyboard.CHATS: command_chat_handler,
        StartKeyboard.ADMINS: command_admin_handler,
        StartKeyboard.HELP: command_help_handler,
        StartKeyboard.REMOVE_ALL_POSTS: command_remove_handler,
    }
