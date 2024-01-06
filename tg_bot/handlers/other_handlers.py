from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tg_bot.keyboards.inline import contact_url_kb
from tg_bot.keyboards.reply import create_reply_kb
from tg_bot.texts.texts import TEXTS

other_router = Router()


# Handler for /contact command
@other_router.message(Command(commands="contact"))
async def contact_command(message: Message):
    text = TEXTS["contact"]
    await message.answer(text, reply_markup=contact_url_kb)


# Handler for /cancel command
@other_router.message(Command(commands="cancel"))
async def cancel_command(message: Message, state: FSMContext):
    await state.clear()
    keyboard = create_reply_kb(2, "student", "interested")
    await message.answer(TEXTS['hello'], reply_markup=keyboard)


@other_router.message()
async def unknown_text(message: Message):
    await message.answer(TEXTS["unknown_text"])
