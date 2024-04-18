from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handlers.start import command_start_handler
from bot.keyboards.reply.admin import AdminMenuKeyboard, get_create_admin_keyboard
from bot.states.admins import AdminStates


router = Router(name="admin")


@router.message(Command("admin"))
async def command_admin_handler(message: Message, state: FSMContext) -> None:
    message_text = "Admin paneliga xush kelibsiz! 🧑‍💼"

    await message.answer(
        text=message_text, reply_markup=AdminMenuKeyboard.get_keyboard()
    )
    await state.set_state(AdminStates.ADMIN)


@router.message(AdminStates.ADMIN, F.text == AdminMenuKeyboard.MENU)
async def admin_menu_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await command_start_handler(message, state)
