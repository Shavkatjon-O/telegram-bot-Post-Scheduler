from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from asgiref.sync import sync_to_async

from bot.models import TelegramAdmin
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


@router.message(AdminStates.ADMIN, F.text == AdminMenuKeyboard.CREATE)
async def admin_create_handler(message: Message, state: FSMContext) -> None:
    message_text = "Yangi adminni tanlang! 🧑‍💼"

    await message.answer(text=message_text, reply_markup=get_create_admin_keyboard())
    await state.set_state(AdminStates.CREATE)


@router.message(AdminStates.CREATE)
async def admin_create_user_handler(message: Message, state: FSMContext) -> None:

    chat_id = message.user_shared.user_id
    await sync_to_async(TelegramAdmin.objects.create)(chat_id=chat_id)

    message_text = "Admin muvaffaqiyatli qo'shildi! 🧑‍💼"

    await message.answer(text=message_text)
    await state.set_state(AdminStates.ADMIN)
