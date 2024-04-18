from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.reply.admin import AdminMenuKeyboard, get_create_admin_keyboard
from bot.states.admins import AdminStates


router = Router(name="admin")


@router.message(Command("admin"))
async def command_admin_handler(message: Message, state: FSMContext) -> None:

    # TODO: send list of admins

    messsage_text = "Adminlar ro'yxati 🧑‍💼"
    await message.answer(messsage_text, reply_markup=AdminMenuKeyboard.get_keyboard())
