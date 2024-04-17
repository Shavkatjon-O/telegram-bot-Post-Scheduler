from asgiref.sync import sync_to_async

from bot.core.loader import bot
from bot.models import TelegramAdmin


async def notify_admins() -> None:
    admins = await sync_to_async(TelegramAdmin.objects.all)()

    async for admin in admins:

        message_text = (
            "Bot ishga tushdi! 🚀\n\n"
            "Botga xush kelibsiz! 🤖\n\n"
            "Botni ishlatish uchun quyidagi buyruqlardan foydalanishingiz mumkin:\n\n"
            "/start - Botni ishga tushirish\n"
            "/admin - Admin paneliga kirish\n"
            "/chat - Chatlar ro'yxatini ko'rish\n"
            "/post - Post yaratish\n\n"
            "Bot haqida batafsil ma'lumot uchun /help buyrug'ini bering. 📚"
        )
        await bot.send_message(admin.chat_id, text=message_text)
