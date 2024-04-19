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
async def command_admin_handler(message: Message, state: FSMContext): ...
