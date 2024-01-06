from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery, Message
from datetime import datetime
from json import load, loads

from tg_bot.config import Config
from tg_bot.keyboards.inline import compose_keyboard_for_test
from tg_bot.keyboards.reply import create_reply_kb
from tg_bot.texts.texts import TEXTS
from tg_bot.misc.gsheets import GoogleForm_test_result, adding_info_to_sheet, open_worksheet
from tg_bot.misc.states import Users

with open("questions.json", "r", encoding="utf-8") as f:
    questions = load(f)

test_router = Router()

correct_answers = []
user_info = []


# starting test
@test_router.message(Users.Testing, Command("test"))
async def start_test(message: Message, state: FSMContext):
    await message.answer(questions[0]["text"],
                         reply_markup=compose_keyboard_for_test(questions, 0))
    await state.set_state(Users.Testing_in_progress)


# starting test
@test_router.message(Users.Testing_in_progress, Command("test"))
async def start_test_in_progress(message: Message):
    await message.answer(TEXTS["test_already_start"])


# Handler for checking test answers.
@test_router.callback_query(Users.Testing_in_progress, lambda c: True)
async def answer_handler(callback: CallbackQuery, state: FSMContext, config: Config):
    data = loads(callback.data)
    q = data["question"]
    is_correct = questions[q]["correct_answer"] - 1 == data["answer"]

    if is_correct:
        correct_answers.append(q)

    if q + 1 > len(questions) - 1:
        await callback.message.delete()
        keyboard = create_reply_kb(1, "want_more")
        await callback.message.answer(
            f'{TEXTS["after_test"]}<b>{len(correct_answers)} з {len(questions)}</b>.',
            reply_markup=keyboard
        )
        await state.set_state(Users.Interested.state)

        date_time = datetime.now()
        date = date_time.date().strftime('%d.%m.%Y')
        time = date_time.time().strftime('%H:%M')
        date_time = f"{date} {time}"

        test_result = GoogleForm_test_result(
            first_name=callback.from_user.first_name,
            last_name=callback.from_user.last_name,
            username=callback.from_user.username,
            correct_answers=len(correct_answers),
            date=date_time
        )

        google_client_manager = config.misc.google_client_manager
        sheet_name = config.misc.sheet_name
        worksheet_name = config.misc.worksheet_test

        worksheet_test = await open_worksheet(google_client_manager,
                                              sheet_name, worksheet_name)
        await adding_info_to_sheet(worksheet_test, test_result)
        return

    await callback.message.edit_text(
        questions[q + 1]["text"],
        reply_markup=compose_keyboard_for_test(questions, q + 1))


# quiting test
@test_router.message(Users.Testing, Command("finish"))
async def finish_test(message: Message):
    await message.answer(TEXTS["test_not_start"])


# quiting test
@test_router.message(Users.Testing_in_progress, Command("finish"))
async def finish_test_in_progress(message: Message, state: FSMContext):
    keyboard = create_reply_kb(1, "want_more")
    await message.answer(TEXTS["the_end"],
                         reply_markup=keyboard)
    await state.set_state(Users.Interested.state)
