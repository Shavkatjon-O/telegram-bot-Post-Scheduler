from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router(name="chat")


@router.message(Command("chat"))
async def command_chat_handler(message: Message):
    await message.answer("Hello, channel!")
