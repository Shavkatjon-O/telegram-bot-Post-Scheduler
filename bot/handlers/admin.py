from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from asgiref.sync import sync_to_async

from bot.models import TelegramAdmin
from bot.handlers.start import command_start_handler
from bot.keyboards.reply.admin import AdminMenuKeyboard, get_create_admin_keyboard
from bot.states.admins import AdminStates
from bot.core.loader import bot


router = Router(name="admin")


@sync_to_async
def get_admin_list() -> str:
    admins = TelegramAdmin.objects.all()
    if not admins:
        return "🚫 Xozircha adminlar ro'yxati bo'sh!"

    text = "💎 Bot adminlari:\n\n"
    for admin in admins:
        text += f"🆔 {admin.chat_id} - {admin.first_name} - @{admin.username}\n"
    return text


@router.message(Command("admin"))
async def command_admin_handler(message: Message, state: FSMContext):
    text = await get_admin_list()
    markup = AdminMenuKeyboard.get_keyboard()

    await message.answer(text, reply_markup=markup)
    await state.set_state(AdminStates.ADMIN)


@router.message(AdminStates.ADMIN, F.text == AdminMenuKeyboard.MENU)
async def admin_menu_handler(message: Message, state: FSMContext):
    await state.clear()
    await command_start_handler(message, state)


@router.message(AdminStates.ADMIN, F.text == AdminMenuKeyboard.CREATE)
async def create_admin_handler(message: Message, state: FSMContext):

    text = " 📝 Yangi admin qo'shish uchun bot foydalanuvchisini tanlang!"
    markup = get_create_admin_keyboard()

    await message.answer(text, reply_markup=markup)
    await state.set_state(AdminStates.CREATE)
