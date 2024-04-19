from aiogram import Router, F
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from asgiref.sync import sync_to_async

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
