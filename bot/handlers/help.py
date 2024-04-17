from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.core.loader import bot


router = Router(name="help")


@router.message(Command("help"))
async def command_help_handler(message: Message, state=None):
    """Handler for /help command."""

    bot_info = await bot.get_me()

    message_text = (
        "Bot haqida batafsil ma'lumot:\n\n"
        f"🤖 Botning ismi: {bot_info.full_name}\n"
        f"👤 Botning username: @{bot_info.username}\n\n"
        "Botni ishlatish uchun quyidagi buyruqlardan foydalanishingiz mumkin:\n\n"
        "/start - Botni ishga tushirish\n"
        "/admin - Admin paneliga kirish\n"
        "/chat - Chatlar ro'yxatini ko'rish\n"
        "/post - Post yaratish\n\n"
    )
    await message.answer(message_text)
