from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from asgiref.sync import sync_to_async
from loguru import logger

from bot.models import TelegramPost
from bot.filters.admin import AdminFilter
from bot.handlers.start import command_start_handler
from bot.states.admins import PostStates, StartStates

from bot.keyboards.reply.start import StartKeyboard
from bot.keyboards.reply.post import CancelKeyboard


router = Router(name="post")


@router.message(Command("post"), AdminFilter())
async def command_post_handler(message: Message, state: FSMContext):
    text = "Menga postni yuboring 📝"

    await message.answer(text, reply_markup=CancelKeyboard.get_keyboard())
    await state.set_state(PostStates.POST)


@router.message(PostStates.POST, F.text == CancelKeyboard.CANCEL)
async def post_cancel_handler(message: Message, state: FSMContext):
    await command_start_handler(message, state)


@router.message(PostStates.POST)
async def post_handler(message: Message, state: FSMContext):
    await sync_to_async(TelegramPost.objects.create)(
        message_id=message.message_id, from_chat_id=message.chat.id
    )

    text = "Post qabul qilindi ✅"
    await message.answer(text, reply_markup=StartKeyboard.get_keyboard())
    await state.set_state(StartStates.START)
