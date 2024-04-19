from asgiref.sync import sync_to_async
from loguru import logger

from bot.core.loader import scheduler, bot
from bot.models import TelegramChat, TelegramPost


async def send_post() -> None:
    chats = await sync_to_async(TelegramChat.objects.all)()

    async for chat in chats:
        try:
            post = await sync_to_async(TelegramPost.objects.first)()
            await bot.copy_message(chat.chat_id, post.from_chat_id, post.message_id)
            logger.success(f"Post sent to {chat.chat_id}")
        except Exception as e:
            logger.error(e)
