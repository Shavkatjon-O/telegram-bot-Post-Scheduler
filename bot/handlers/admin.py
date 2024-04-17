from aiogram import Router, F
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.reply.admin import AdminKeyboards, CancelKeyboard

from bot.core.loader import bot
from bot.states.admins import AdminStates
from bot.handlers.start import command_start_handler
from bot.models import TelegramAdmin

from bot.filters.admin import AdminFilter
from bot.filters.number import NumberFilter

from asgiref.sync import sync_to_async
from loguru import logger


router = Router(name="admin")


@router.message(Command("admin"), AdminFilter())
async def command_admin_handler(message: Message, state: FSMContext) -> None:
    """Handler for the /admin command."""

    telegram_admins = await sync_to_async(TelegramAdmin.objects.all)()

    message_text = "Adminlar ro'yxati 💎\n\n"

    async for admin in telegram_admins:
        if not admin.username:
            try:
                chat_info = await bot.get_chat(admin.chat_id)

                admin.username = chat_info.username
                admin.first_name = chat_info.first_name
                admin.last_name = chat_info.last_name

                await sync_to_async(admin.save)()
            except Exception as e:
                logger.error(e)
                continue

        message_text += f"🆔 <code>{admin.chat_id}</code> - {admin.first_name}\n\n"

    await message.answer(text=message_text, reply_markup=AdminKeyboards.get_keyboard())
    await state.set_state(AdminStates.ADMIN)


@router.message(AdminStates.ADMIN, F.text == AdminKeyboards.MENU)
async def return_to_menu_handler(message: Message, state: FSMContext) -> None:
    """Handler for returning user back to the main menu."""

    await state.clear()
    await command_start_handler(message, state)


@router.message(
    AdminStates.ADMIN,
    or_f(F.text == AdminKeyboards.CREATE, F.text == AdminKeyboards.DELETE),
)
async def create_or_delete_handler(message: Message, state: FSMContext) -> None:
    """Handler for creating or deleting admin."""

    message_text = "Foydalanuvchi identifikatorini kiriting 🆔"
    await message.answer(text=message_text, reply_markup=CancelKeyboard.get_keyboard())

    await state.update_data(action=message.text)
    await state.set_state(AdminStates.CREATE_OR_DELETE)


@router.message(AdminStates.CREATE_OR_DELETE, F.text == CancelKeyboard.CANCEL)
async def cancel_action_handler(message: Message, state: FSMContext) -> None:
    """Handler for cancelling the action."""

    await state.clear()
    await command_admin_handler(message, state)


@router.message(AdminStates.CREATE_OR_DELETE, NumberFilter())
async def create_or_delete_action_handler(message: Message, state: FSMContext) -> None:
    """Handler for creating or deleting admin."""

    data = await state.get_data()
    action = data.get("action")

    try:
        chat_id = message.text
        chat_info = await bot.get_chat(chat_id)
    except Exception as e:
        await message.answer(text="Foydalanuvchi topilmadi. 😔")
        logger.error(e)
        return

    if chat_info.id == message.from_user.id:
        await message.answer(
            text="Siz o'zingizni qo'shish yoki o'chirish mumkin emas. 😔"
        )
        return

    if action == AdminKeyboards.CREATE:
        try:
            await sync_to_async(TelegramAdmin.objects.create)(
                chat_id=chat_id,
                username=chat_info.username,
                first_name=chat_info.first_name,
                last_name=chat_info.last_name,
            )
            await message.answer(text="Foydalanuvchi adminlar ro'yxatiga qo'shildi. 🎉")
        except Exception as e:
            await message.answer(text="Foydalanuvchi allaqachon admin. 😔")

            logger.error(e)
            return
    elif action == AdminKeyboards.DELETE:
        try:
            telegram_admin = await sync_to_async(TelegramAdmin.objects.get)(
                chat_id=chat_id
            )
            if telegram_admin:
                await sync_to_async(telegram_admin.delete)()

            await message.answer(
                text="Foydalanuvchi adminlar ro'yxatidan o'chirildi. 🎉"
            )
        except Exception as e:
            await message.answer(text="Foydalanuvchi admin emas. 😔")

            logger.error(e)
            return
    else:
        await message.answer(text="Xatolik yuz berdi. Qayta urinib ko'ring. 😔")

    await state.clear()
    await command_admin_handler(message, state)
