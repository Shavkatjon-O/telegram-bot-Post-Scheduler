from asgiref.sync import sync_to_async

from bot.core.loader import bot
from bot.models import TelegramAdmin


async def notify_admins() -> None:
    admins = await sync_to_async(TelegramAdmin.objects.all)()

    async for admin in admins:
        message_text = "Hello, I'm alive!"
        await bot.send_message(admin.chat_id, text=message_text)
