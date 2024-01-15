from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from tg_bot.config import Config
from tg_bot.keyboards.reply import create_reply_kb
from tg_bot.misc.gsheets import open_worksheet, save_user, save_user_status
from tg_bot.misc.states import Users
from tg_bot.misc import texts

start_router = Router()


# hendler for /start command
@start_router.message(StateFilter(default_state), CommandStart())
async def cmd_start(message: Message, config: Config):
    google_client_manager = config.misc.google_client_manager
    sheet_name = config.misc.sheet_name
    worksheet_name = config.misc.worksheet_users
    worksheet_users = await open_worksheet(google_client_manager,
                                           sheet_name, worksheet_name)
    await save_user(message, worksheet_users)
    keyboard = create_reply_kb(2, texts.STUDENT, texts.INTERESTED)
    await message.answer(texts.HELLO, reply_markup=keyboard)


# Handler for answer if this is a people, who interested in styding
@start_router.message(F.text == texts.INTERESTED)
async def interested_start(message: Message, state: FSMContext, config: Config):
    google_client_manager = config.misc.google_client_manager
    sheet_name = config.misc.sheet_name
    worksheet_name = config.misc.worksheet_users
    worksheet_users = await open_worksheet(google_client_manager,
                                           sheet_name, worksheet_name)
    await save_user_status(message, 5, worksheet_users)
    keyboard = create_reply_kb(1, texts.FORMAT_EDUCATION,
                               texts.PRICE, texts.ENGLISH_LEVEL)
    await message.answer(text=texts.INTERESTED_Q1, reply_markup=keyboard)
    await state.set_state(Users.Interested.state)


# Handler for answer if this is a student
@start_router.message(F.text == texts.STUDENT)
async def student_start(message: Message, state: FSMContext, config: Config):
    google_client_manager = config.misc.google_client_manager
    sheet_name = config.misc.sheet_name
    worksheet_name = config.misc.worksheet_users
    worksheet_users = await open_worksheet(google_client_manager,
                                           sheet_name, worksheet_name)
    await save_user_status(message, 5, worksheet_users)
    keyboard = create_reply_kb(1, texts.REVIEW, texts.WANT_PAY, texts.WANT_NUM_LESSONS)
    await message.answer(texts.STUDENT_Q1, reply_markup=keyboard)
    await state.set_state(Users.Student.state)
