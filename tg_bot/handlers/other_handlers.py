from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tg_bot.keyboards.inline import create_inline_url_kb
from tg_bot.keyboards.reply import create_reply_kb
from tg_bot.misc import texts

other_router = Router()


# Handler for /contact command
@other_router.message(Command(commands="contact"))
async def contact_command(message: Message):
    contact_url_kb = create_inline_url_kb(
        text=texts.CONTACT_URL_TEXT,
        url=texts.CONTACT_URL
    )
    await message.answer(texts.CONTACT, reply_markup=contact_url_kb)


# Handler for /cancel command
@other_router.message(Command(commands="cancel"))
async def cancel_command(message: Message, state: FSMContext):
    await state.clear()
    keyboard = create_reply_kb(2, texts.STUDENT, texts.INTERESTED)
    await message.answer(texts.HELLO, reply_markup=keyboard)


@other_router.message()
async def unknown_text(message: Message):
    await message.answer(texts.UNKNOWN_TEXT)
