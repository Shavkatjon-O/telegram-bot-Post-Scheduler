from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from asgiref.sync import sync_to_async

from bot.models import TelegramAdmin
from bot.handlers.start import command_start_handler
from bot.keyboards.reply.admin import AdminMenuKeyboard, get_create_admin_keyboard
from bot.states.admins import AdminStates


router = Router(name="admin")


@router.message(Command("admin"))
async def command_admin_handler(message: Message, state: FSMContext) -> None:
    """Handler for the /admin command."""

    message_text = "Admin paneliga xush kelibsiz! 🧑‍💼"

    await message.answer(
        text=message_text, reply_markup=AdminMenuKeyboard.get_keyboard()
    )
    await state.set_state(AdminStates.ADMIN)


@router.message(AdminStates.ADMIN, F.text == AdminMenuKeyboard.MENU)
async def admin_menu_handler(message: Message, state: FSMContext) -> None:
    """Handler for the "Menu" button in the admin panel."""

    await state.clear()
    await command_start_handler(message, state)


@router.message(AdminStates.ADMIN, F.text == AdminMenuKeyboard.CREATE)
async def admin_create_handler(message: Message, state: FSMContext) -> None:
    """Handler for the "Create" button in the admin panel."""

    message_text = "Yangi adminni tanlang! 🧑‍💼"

    await message.answer(text=message_text, reply_markup=get_create_admin_keyboard())
    await state.set_state(AdminStates.CREATE)


@router.message(AdminStates.CREATE)
async def admin_create_user_handler(message: Message, state: FSMContext) -> None:
    """Handler for creating a new admin."""

    chat_id = message.user_shared.user_id

    admin, created = await sync_to_async(TelegramAdmin.objects.get_or_create)(
        chat_id=chat_id
    )

    if not created:
        message_text = "Bu foydalanuvchi allaqachon admin! ❌"
    else:
        message_text = "Admin muvaffaqiyatli yaratildi! ✅"

    await message.answer(
        text=message_text, reply_markup=AdminMenuKeyboard.get_keyboard()
    )
    await state.set_state(AdminStates.ADMIN)


@router.message(AdminStates.ADMIN, F.text == AdminMenuKeyboard.DELETE)
async def admin_delete_handler(message: Message, state: FSMContext) -> None:
    """Handler for the "Delete" button in the admin panel."""

    admins = await sync_to_async(TelegramAdmin.objects.all)()
    message_text = "O'chirish uchun foydalanuvchini tanlang! 🧑‍💼"

    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=str(admin.chat_id))] async for admin in admins],
        resize_keyboard=True,
    )
    await message.answer(text=message_text, reply_markup=markup)
    await state.set_state(AdminStates.DELETE)


@router.message(AdminStates.DELETE)
async def admin_delete_user_handler(message: Message, state: FSMContext) -> None:
    """Handler for deleting an admin."""

    try:
        chat_id = int(message.text)
        admin = await sync_to_async(TelegramAdmin.objects.get)(chat_id=chat_id)
        await sync_to_async(admin.delete)()

        message_text = "Admin o'chirildi! ✅"
        await message.answer(
            text=message_text, reply_markup=AdminMenuKeyboard.get_keyboard()
        )
    except Exception:
        message_text = "Foydalanuvchi topilmadi! ❌"
        await message.answer(
            text=message_text, reply_markup=AdminMenuKeyboard.get_keyboard()
        )
    await state.set_state(AdminStates.ADMIN)
