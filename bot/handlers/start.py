from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.reply.start import StartKeyboard, get_menu_buttons
from bot.states.admins import StartStates


router = Router(name="start")


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """Handler for the /start command."""

    await message.answer(
        "Salom, botga xush kelibsiz!", reply_markup=StartKeyboard.get_keyboard()
    )
    await state.set_state(StartStates.START)


@router.message(StartStates.START, F.text == get_menu_buttons().keys())
async def start_handler(message: Message, state: FSMContext) -> None:
    """Handler for the start menu buttons."""
    buttons = get_menu_buttons()

    await state.clear()
    await buttons[message.text](message, state)
