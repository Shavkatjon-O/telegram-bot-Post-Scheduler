from aiogram.filters import BaseFilter
from aiogram.types import Message


class NumberFilter(BaseFilter):
    """Allows only numbers with or without a dot."""

    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return False

        try:
            float(message.text)
        except ValueError:
            await message.answer("Это не число. Попробуйте еще раз.")

            return False
        else:
            return True
