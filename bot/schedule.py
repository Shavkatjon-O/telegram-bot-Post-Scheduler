from asgiref.sync import sync_to_async
from loguru import logger

from bot.core.loader import scheduler, bot
from bot.models import TelegramChat


async def send_post() -> None:
    chats = await sync_to_async(TelegramChat.objects.all)()

    async for chat in chats:
        try:
            await bot.send_message(chat_id=chat.chat_id, text="Hello, World!")
        except Exception as e:
            logger.error(f"Error while sending message to chat {chat.chat_id}: {e}")
