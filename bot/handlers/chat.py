from aiogram import Router, F
from aiogram.filters import Command, or_f
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


@router.message(
    ChatStates.CHAT,
    or_f(F.text == ChatKeyboard.CREATE, F.text == ChatKeyboard.DELETE),
)
async def create_or_delete_handler(message: Message, state: FSMContext) -> None:
    """Handler for creating or deleting chats."""

    message_text = "Kanal @nomini kiriting 📝"
    await message.answer(text=message_text, reply_markup=CancelKeyboard.get_keyboard())

    await state.update_data(action=message.text)
    await state.set_state(ChatStates.CREATE_OR_DELETE)


@router.message(ChatStates.CREATE_OR_DELETE, F.text == CancelKeyboard.CANCEL)
async def cancel_action_handler(message: Message, state: FSMContext) -> None:
    """Handler for cancelling the action."""

    await state.clear()
    await command_chat_handler(message, state)
