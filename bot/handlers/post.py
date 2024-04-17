from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router(name="post")


@router.message(Command("post"))
async def command_post_handler(message: Message, state=None):
    await message.answer("Hello, post!")
