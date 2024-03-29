from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery, Message
from datetime import datetime
from json import load, loads

from tg_bot.config import Config
from tg_bot.keyboards.inline import compose_keyboard_for_test
from tg_bot.keyboards.reply import create_reply_kb
from tg_bot.misc import texts
from tg_bot.misc.gsheets import open_worksheet
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
    await message.answer(texts.TEST_ALREADY_START)


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
        keyboard = create_reply_kb(1, texts.WANT_MORE)
        await callback.message.answer(
            f'{texts.AFTER_TEST}<b>{len(correct_answers)} з {len(questions)}</b>.',
            reply_markup=keyboard
        )
        await state.set_state(Users.Interested.state)

        test_result = {
            "first_name": callback.from_user.first_name,
            "last_name": callback.from_user.last_name,
            "username": callback.from_user.username,
            "correct_answers": len(correct_answers),
            "date": datetime.now().strftime('%Y.%m.%d %H:%M')
        }

        google_client_manager = config.misc.google_client_manager
        sheet_name = config.misc.sheet_name
        worksheet_name = config.misc.worksheet_test

        worksheet_test = await open_worksheet(google_client_manager,
                                              sheet_name, worksheet_name)
        await worksheet_test.append_row(list(test_result.values()))
        return

    await callback.message.edit_text(
        questions[q + 1]["text"],
        reply_markup=compose_keyboard_for_test(questions, q + 1))


# quiting test
@test_router.message(Users.Testing, Command("finish"))
async def finish_test(message: Message):
    await message.answer(texts.TEST_NOT_START)


# quiting test
@test_router.message(Users.Testing_in_progress, Command("finish"))
async def finish_test_in_progress(message: Message, state: FSMContext):
    keyboard = create_reply_kb(1, texts.WANT_MORE)
    await message.answer(texts.TEST_THE_END,
                         reply_markup=keyboard)
    await state.set_state(Users.Interested.state)
