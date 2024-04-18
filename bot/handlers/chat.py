from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.states.admins import ChatStates
from bot.keyboards.reply.chat import ChatKeyboard, CancelKeyboard
from bot.handlers.start import command_start_handler


router = Router(name="chat")


@router.message(Command("chat"))
async def command_chat_handler(message: Message, state: FSMContext) -> None:
    """Handler for the /chat command."""

    # TODO: send list of channels

    message_text = "Kanal ro'yxati 💎\n\n"

    await message.answer(text=message_text, reply_markup=ChatKeyboard.get_keyboard())
    await state.set_state(ChatStates.CHAT)


@router.message(ChatStates.CHAT, F.text == ChatKeyboard.MENU)
async def return_to_menu_handler(message: Message, state: FSMContext) -> None:
    """Handler for returning user back to the main menu."""

    await state.clear()
    await command_start_handler(message, state)
