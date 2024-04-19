from aiogram import Router, F
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from asgiref.sync import sync_to_async

from loguru import logger

from bot.states.admins import ChatStates
from bot.keyboards.reply.chat import ChatMenuKeyboard, SelectChatKeyboard
from bot.handlers.start import command_start_handler
from bot.models import TelegramChat


router = Router(name="chat")


@sync_to_async
def get_chat_list() -> str:
    chats = TelegramChat.objects.all()
    if not chats:
        return "🚫 Xozircha chatlar ro'yxati bo'sh!"

    text = "💎 Bot chatlari:\n\n"
    for chat in chats:
        text += f"🆔 {chat.chat_id} - {chat.title}\n"
    return text


@router.message(Command("chat"))
async def command_chat_handler(message: Message, state: FSMContext):
    text = await get_chat_list()
    markup = ChatMenuKeyboard.get_keyboard()

    await message.answer(text, reply_markup=markup)
    await state.set_state(ChatStates.CHAT)


@router.message(ChatStates.CHAT, F.text == ChatMenuKeyboard.MENU)
async def chat_menu_handler(message: Message, state: FSMContext):
    await state.clear()
    await command_start_handler(message, state)


@router.message(ChatStates.CHAT, F.text == ChatMenuKeyboard.CREATE)
async def chat_create_handler(message: Message, state: FSMContext):
    text = "📝 Kanal yoki guruhni tanlang"
    markup = SelectChatKeyboard.get_keyboard()

    await message.answer(text, reply_markup=markup)
    await state.set_state(ChatStates.CREATE)


@router.message(ChatStates.CREATE, F.text == "Bekor qilish ❌")
async def chat_cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await command_chat_handler(message, state)


@router.message(ChatStates.CREATE)
async def chat_selected_handler(message: Message, state: FSMContext):
    chat_id = message.chat_shared.chat_id

    try:
        chat_info = await message.bot.get_chat(chat_id)
        await sync_to_async(TelegramChat.objects.create)(
            chat_id=chat_id, title=chat_info.title
        )
        text = "✅ Chat muvaffaqiyatli qo'shildi!"
    except Exception as e:
        text = "❌ Chat qo'shishda xatolik yuz berdi!"
        logger.error(f"Error: {e}")

    chat_list = await get_chat_list()
    await message.answer(chat_list)

    await message.answer(text, reply_markup=ChatMenuKeyboard.get_keyboard())
    await state.set_state(ChatStates.CHAT)
