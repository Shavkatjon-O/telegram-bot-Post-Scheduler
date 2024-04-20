from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from asgiref.sync import sync_to_async

from loguru import logger

from bot.keyboards.reply.admin import (
    AdminMenuKeyboard,
    get_create_admin_keyboard,
    get_delete_admin_keyboard,
)
from bot.models import TelegramAdmin
from bot.handlers.start import command_start_handler
from bot.states.admins import AdminStates
from bot.filters.admin import AdminFilter
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


@router.message(Command("admin"), AdminFilter())
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
async def create_select_admin_handler(message: Message, state: FSMContext):
    text = " 📝 Yangi admin qo'shish uchun bot foydalanuvchisini tanlang!"
    markup = get_create_admin_keyboard()

    await message.answer(text, reply_markup=markup)
    await state.set_state(AdminStates.CREATE)


@router.message(AdminStates.CREATE)
async def create_admin_handler(message: Message, state: FSMContext):
    chat_id = message.user_shared.user_id
    chat_info = await bot.get_chat(chat_id)

    try:
        await sync_to_async(TelegramAdmin.objects.create)(
            chat_id=chat_info.id,
            first_name=chat_info.first_name,
            last_name=chat_info.last_name,
            username=chat_info.username,
        )
        text = f"🆔 {chat_info.id} - {chat_info.first_name} - @{chat_info.username} admin qo'shildi!"
    except Exception:
        text = "❌ Xatolik yuz berdi! Admin qo'shilmadi!"

    await message.answer(text, reply_markup=AdminMenuKeyboard.get_keyboard())
    await state.set_state(AdminStates.ADMIN)


@router.message(AdminStates.ADMIN, F.text == AdminMenuKeyboard.DELETE)
async def delete_select_admin_handler(message: Message, state: FSMContext):
    markup = await get_delete_admin_keyboard()
    text = "🗑 O'chirish uchun admin tanlang!"

    await message.answer(text=text, reply_markup=markup)
    await state.set_state(AdminStates.DELETE)


@router.message(AdminStates.DELETE, F.text == "Orqaga 🔙")
async def back_to_admin_menu_handler(message: Message, state: FSMContext):
    await state.clear()
    await command_admin_handler(message, state)


@router.message(AdminStates.DELETE)
async def delete_admin_handler(message: Message, state: FSMContext):
    try:
        chat_id = int(message.text.split(" - ")[0])

        if chat_id == message.from_user.id:
            await message.answer("❌ Siz o'zingizni o'chirib yubormang!")
            return

        admin = await sync_to_async(TelegramAdmin.objects.get)(chat_id=chat_id)
        await sync_to_async(admin.delete)()

        text = f"🆔 {admin.chat_id} - {admin.first_name} - @{admin.username} admin o'chirildi!"
    except Exception as e:
        text = "❌ Xatolik yuz berdi! Admin o'chirilmadi!"
        logger.error(f"Error: {e}")

    await message.answer(text, reply_markup=AdminMenuKeyboard.get_keyboard())
    await state.set_state(AdminStates.ADMIN)
