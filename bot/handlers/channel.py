from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router(name="channel")


@router.message(Command("channel"))
async def command_channel_handler(message: Message):
    await message.answer("Hello, channel!")
