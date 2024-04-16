import os
import django
import environ

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.conf import settings

from bot.core.loader import dp, bot
from bot.handlers import get_handlers_rounter

from loguru import logger


async def on_startup() -> None:
    logger.info("Starting bot...")

    dp.include_router(get_handlers_rounter())

    bot_info = await bot.get_me()

    logger.info(f"Name     - {bot_info.full_name}")
    logger.info(f"Username - @{bot_info.username}")
    logger.info(f"ID       - {bot_info.id}")

    states: dict[bool | None, str] = {
        True: "Enabled",
        False: "Disabled",
        None: "Unknown (This's not a bot)",
    }

    logger.info(f"Groups Mode  - {states[bot_info.can_join_groups]}")
    logger.info(f"Privacy Mode - {states[not bot_info.can_read_all_group_messages]}")
    logger.info(f"Inline Mode  - {states[bot_info.supports_inline_queries]}")

    logger.info("Bot started!")


async def on_shutdown() -> None:
    logger.info("Stopping bot...")

    await dp.storage.close()
    await dp.fsm.storage.close()

    await bot.delete_webhook()
    await bot.session.close()

    logger.info("Bot stopped!")


async def main() -> None:
    if not settings.DEBUG:
        logger.add(
            "logs/bot/telegram_bot.log",
            level="DEBUG",
            format="{time} | {level} | {module}:{function}:{line} | {message}",
            rotation="100 KB",
            compression="zip",
        )

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    import uvloop

    uvloop.run(main())
