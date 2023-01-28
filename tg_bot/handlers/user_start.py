from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from tg_bot.keyboards.reply import create_reply_kb
from tg_bot.services.servives import select_user
from tg_bot.texts.texts import TEXTS
from tg_bot.misc.gsheets import save_user


# hendler for /start command
async def cmd_start(message: Message, state: FSMContext):
    await state.finish()
    user = select_user(message.from_user.id)
    save_user(user)
    keyboard = create_reply_kb(2, "student", "interested")
    await message.answer(TEXTS['hello'], reply_markup=keyboard)


def register_cmd_start(dp: Dispatcher):
    dp.register_message_handler(cmd_start,
                                commands=["start"],
                                state="*")
