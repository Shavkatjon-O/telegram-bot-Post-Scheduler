from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router(name="admin")


@router.message(Command("admin"))
async def command_admin_handler(message: Message):
    await message.answer("Hello, admin!")
