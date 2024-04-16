from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message


router = Router(name="start")


@router.message(CommandStart())
async def command_start_handler(message: Message, state=None) -> None:
    await message.answer(f"Hello! I'm a bot! {message.from_user.id}")
