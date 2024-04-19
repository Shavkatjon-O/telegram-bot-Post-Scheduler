from aiogram.types import ReplyKeyboardMarkup, KeyboardButtonRequestChat
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton

from asgiref.sync import sync_to_async
from bot.models import TelegramChat


class ChatMenuKeyboard:
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


class SelectChatKeyboard:
    CHANNEL = "Kanalni tanlash 📝"
    GROUP = "Guruhni tanlash 📝"
    CANCEL = "Bekor qilish ❌"

    @classmethod
    def get_keyboard(cls) -> ReplyKeyboardMarkup:
        """Get select chat keyboard."""

        buttons = [
            [
                KeyboardButton(
                    text=cls.CHANNEL,
                    request_chat=KeyboardButtonRequestChat(
                        request_id=1,
                        user_is_bot=False,
                        chat_is_channel=True,
                        chat_is_forum=False,
                    ),
                ),
            ],
            [
                KeyboardButton(
                    text=cls.GROUP,
                    request_chat=KeyboardButtonRequestChat(
                        request_id=2,
                        user_is_bot=False,
                        chat_is_channel=False,
                        chat_is_forum=False,
                    ),
                ),
            ],
            [KeyboardButton(text=cls.CANCEL)],
        ]

        keyboard = ReplyKeyboardBuilder(markup=buttons)
        keyboard.adjust(2, 1)

        return keyboard.as_markup(
            resize_keyboard=True,
        )


@sync_to_async
def get_delete_chat_keyboard() -> ReplyKeyboardMarkup:
    chats = TelegramChat.objects.all()

    buttons = [
        [KeyboardButton(text=f"{chat.chat_id} - {chat.title}")] for chat in chats
    ]
    buttons.append([KeyboardButton(text="Orqaga 🔙")])

    keyboard = ReplyKeyboardBuilder(markup=buttons)
    keyboard.adjust(1, 1)

    return keyboard.as_markup(resize_keyboard=True)
