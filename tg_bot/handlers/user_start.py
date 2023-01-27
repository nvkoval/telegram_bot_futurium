from aiogram import Dispatcher
from aiogram.types import Message
from tg_bot.keyboards.inline import create_inline_kb
from tg_bot.services.servives import select_user
from tg_bot.texts.texts import TEXTS
from tg_bot.misc.gsheets import save_user


# hendler for /start command
async def cmd_start(message: Message):
    user = select_user(message.from_user.id)
    save_user(user)
    text = TEXTS['hello']
    keyboard = create_inline_kb(2, "student", "interested")
    await message.answer(text, reply_markup=keyboard)


def register_cmd_start(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"])
