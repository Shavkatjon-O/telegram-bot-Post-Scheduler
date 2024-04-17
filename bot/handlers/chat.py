from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


from bot.keyboards.reply.chat import ChatKeyboard


router = Router(name="chat")


@router.message(Command("chat"))
async def command_chat_handler(message: Message, state=None):
    await message.answer("Hello, channel!", reply_markup=ChatKeyboard.get_keyboard())
