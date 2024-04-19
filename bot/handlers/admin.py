from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from asgiref.sync import sync_to_async

from bot.models import TelegramAdmin
from bot.filters.number import NumberFilter
from bot.handlers.start import command_start_handler
from bot.keyboards.reply.admin import AdminMenuKeyboard, get_create_admin_keyboard
from bot.states.admins import AdminStates
from bot.core.loader import bot


router = Router(name="admin")


async def get_admins_message() -> str:
    """Returns a list of all admins in the database."""

    text = "Adminlar ro'yxati 💎\n\n"
    admins = await sync_to_async(TelegramAdmin.objects.all)()

    async for admin in admins:
        if not admin.username:
            try:
                chat = await bot.get_chat(admin.chat_id)
            except Exception:
                continue

            admin.username = chat.username
            admin.first_name = chat.first_name
            admin.last_name = chat.last_name

        text += f"🆔 {admin.chat_id} - {admin.first_name}\n\n"

    await sync_to_async(TelegramAdmin.objects.bulk_update)(
        admins, ["username", "first_name", "last_name"]
    )
    return text


@router.message(Command("admin"))
async def command_admin_handler(message: Message, state: FSMContext):
    """Handler for the /admin command."""

    message_text = await get_admins_message()
    markup = AdminMenuKeyboard.get_keyboard()

    await message.answer(text=message_text, reply_markup=markup)
    await state.set_state(AdminStates.ADMIN)


@router.message(AdminStates.ADMIN, F.text == AdminMenuKeyboard.MENU)
async def admin_menu_handler(message: Message, state: FSMContext):
    """Handler for the "Menu" button in the admin panel."""

    await state.clear()
    await command_start_handler(message, state)


@router.message(AdminStates.ADMIN, F.text == AdminMenuKeyboard.CREATE)
async def admin_create_handler(message: Message, state: FSMContext):
    """Handler for the "Create" button in the admin panel."""

    message_text = "Yangi adminni tanlang! 🧑‍💼"
    markup = get_create_admin_keyboard()

    await message.answer(text=message_text, reply_markup=markup)
    await state.set_state(AdminStates.CREATE)


@router.message(AdminStates.CREATE)
async def admin_create_user_handler(message: Message, state: FSMContext):
    """Handler for creating a new admin."""

    try:
        chat_id = message.user_shared.user_id
        await sync_to_async(TelegramAdmin.objects.create)(chat_id=chat_id)

        message_text = "Admin muvaffaqiyatli yaratildi! ✅"
    except Exception as e:
        message_text = "Bu foydalanuvchi allaqachon admin! ❌"

    markup = AdminMenuKeyboard.get_keyboard()

    await message.answer(text=message_text, reply_markup=markup)
    await state.set_state(AdminStates.ADMIN)


@router.message(AdminStates.ADMIN, F.text == AdminMenuKeyboard.DELETE)
async def admin_delete_handler(message: Message, state: FSMContext) -> None:
    """Handler for the "Delete" button in the admin panel."""

    admins = await sync_to_async(TelegramAdmin.objects.all)()
    keyboard = [[KeyboardButton(text=str(admin.chat_id))] async for admin in admins]

    message_text = "O'chirish uchun foydalanuvchini tanlang! 🧑‍💼"
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

    await message.answer(text=message_text, reply_markup=markup)
    await state.set_state(AdminStates.DELETE)


@router.message(AdminStates.DELETE, NumberFilter())
async def admin_delete_user_handler(message: Message, state: FSMContext) -> None:
    """Handler for deleting an admin."""

    try:
        admin = await sync_to_async(TelegramAdmin.objects.get)(chat_id=message.text)
        await sync_to_async(admin.delete)()

        message_text = "Admin o'chirildi! ✅"
    except Exception:
        message_text = "Foydalanuvchi topilmadi! ❌"

    markup = AdminMenuKeyboard.get_keyboard()

    await message.answer(text=message_text, reply_markup=markup)
    await state.set_state(AdminStates.ADMIN)
