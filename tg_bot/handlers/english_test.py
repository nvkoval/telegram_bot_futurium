from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message
from json import loads
from json import load

from tg_bot.keyboards.inline import compose_markup_for_test
from tg_bot.keyboards.reply import create_reply_kb
from tg_bot.texts.texts import TEXTS
from tg_bot.misc.gsheets import adding_info_spreadsheet
from tg_bot.misc.states import Users

questions = load(open("questions.json", "r", encoding="utf-8"))

# help variables
correct_answers = []
user_info = []
is_in_progress = False


# Handler на кнопку english test
async def start_eng_test(message: Message, state: FSMContext):
    await message.answer(TEXTS["test_hello"], parse_mode="MarkdownV2")
    await state.set_state(Users.Testing.state)


# Handler for checking test answers.
async def answer_handler(callback: CallbackQuery, state: FSMContext):
    data = loads(callback.data)
    is_in_progress = True
    q = data["question"]
    is_correct = questions[q]["correct_answer"] - 1 == data["answer"]
    (callback.from_user.id)
    if is_correct:
        correct_answers.append(q)
    if q + 1 > len(questions) - 1:
        await callback.message.delete()
        keyboard = create_reply_kb(1, "want_more")
        await callback.message.answer(
            f"Ви пройшли тестування\\! \n✅ Правильних відповідей\\: *{len(correct_answers)} з {len(questions)}*\\.",
            reply_markup=keyboard,
            parse_mode="MarkdownV2"
        )
        await state.set_state(Users.Interested.state)

        user = [
            callback.from_user.id,
            len(correct_answers)
            ]

        adding_info_spreadsheet(user)
        return

    await callback.message.edit_text(questions[q + 1]["text"],
                                     reply_markup=compose_markup_for_test(q + 1),
                                     parse_mode="MarkdownV2")


# starting test
async def go_handler(message: Message, state: FSMContext):
    if is_in_progress:
        await message.answer("🚫 Ви не можете почати тест, тому що *ви вже його проходите*\\.",
                             parse_mode="MarkdownV2")
        return
    else:
        await message.answer(questions[0]["text"],
                             reply_markup=compose_markup_for_test(0),
                             parse_mode="MarkdownV2")


# quiting test
async def quit_handler(message: Message, state: FSMContext):
    if is_in_progress is False:
        await message.answer("❗️Ви ще *не почали тест*\\.",
                             parse_mode="MarkdownV2")
        return
    keyboard = create_reply_kb(1, "want_more")
    await message.answer("✅ Ви *закінчили тест*\\.",
                         parse_mode="MarkdownV2", reply_markup=keyboard)
    await state.set_state(Users.Interested.state)


def register_eng_level_test(dp: Dispatcher):
    dp.register_message_handler(start_eng_test,
                                text=TEXTS["english_level"],
                                state="*")

    dp.register_message_handler(go_handler,
                                commands=["test"],
                                state=Users.Testing)

    dp.register_message_handler(quit_handler,
                                commands=["finish"],
                                state=Users.Testing)

    dp.register_callback_query_handler(answer_handler,
                                       lambda c: True,
                                       state=Users.Testing)
