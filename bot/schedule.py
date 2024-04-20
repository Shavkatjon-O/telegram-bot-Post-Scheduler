import asyncio

from asgiref.sync import sync_to_async
from loguru import logger

from bot.core.loader import bot
from bot.models import TelegramChat, TelegramPost


async def send_posts() -> None:
    while True:
        chats = await sync_to_async(TelegramChat.objects.all)()
        posts = await sync_to_async(TelegramPost.objects.all)()

        async for post in posts:
            async for chat in chats:
                try:
                    await bot.copy_message(
                        chat_id=chat.chat_id,
                        from_chat_id=post.from_chat_id,
                        message_id=post.message_id,
                    )
                    logger.info(f"Post sent to {chat.chat_id}")
                except Exception as e:
                    logger.error(e)
                    continue
            await asyncio.sleep(5)
