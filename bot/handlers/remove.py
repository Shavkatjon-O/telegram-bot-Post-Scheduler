from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from asgiref.sync import sync_to_async

from bot.filters.admin import AdminFilter
from bot.keyboards.reply.start import StartKeyboard
from bot.states.admins import RemoveStates, StartStates
from bot.keyboards.reply.remove import ConfirmKeyboard
from bot.handlers.start import command_start_handler
from bot.models import TelegramPost


router = Router(name="remove")


@router.message(Command("remove"), AdminFilter())
async def command_remove_handler(message: Message, state: FSMContext):

    await message.answer(
        "🗑 O'chirish uchun postni yuboring!",
        reply_markup=ConfirmKeyboard.get_keyboard(),
    )
    await state.set_state(RemoveStates.REMOVE)


@router.message(RemoveStates.REMOVE, F.text == ConfirmKeyboard.CANCEL)
async def remove_cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await command_start_handler(message, state)


@router.message(RemoveStates.REMOVE, F.text == ConfirmKeyboard.CONFIRM)
async def remove_confirm_handler(message: Message, state: FSMContext):
    await sync_to_async(TelegramPost.objects.all().delete)()

    await message.answer(
        "✅ Postlar o'chirildi!", reply_markup=StartKeyboard.get_keyboard()
    )
    await state.set_state(StartStates.START)
