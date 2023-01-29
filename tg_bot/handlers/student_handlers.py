from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tg_bot.keyboards.inline import futurium_tg_kb, review_kb
from tg_bot.keyboards.reply import create_reply_kb, finish_rkb_student
from tg_bot.misc.gsheets import worksheet_num, num_class_left, get_price
from tg_bot.misc.gsheets import save_message, save_user_status
from tg_bot.misc.states import Users
from tg_bot.texts.texts import TEXTS


# Handler for answer if this is a student
async def student_start(message: Message, state: FSMContext):
    save_user_status(message, 5)
    keyboard = create_reply_kb(1, "review", "want_pay", "want_num_lesson")
    await message.answer(TEXTS["student_q1"], reply_markup=keyboard)
    await state.set_state(Users.Student.state)


# Handler for enter name
async def student_enter_name(message: Message, state: FSMContext):
    await message.answer(TEXTS["enter_name"], parse_mode="HTML")
    await state.set_state(Users.Student_name.state)


# Handler for incorrect name
async def warning_not_name(message: Message):
    await message.answer(text=TEXTS["enter_name_error"], parse_mode="HTML")


# Handler for correct name and get a number of lessons
async def student_lessons_left(message: Message, state: FSMContext):
    name = message.text
    if name in worksheet_num.col_values(2):
        save_message(message, 3)
        class_left = int(num_class_left(name))
        keyboard = create_reply_kb(1, "yes", "later")
        if class_left >= 0:
            text = f'{TEXTS["left_class_start"]}{class_left}{TEXTS["left_class_paid"]}'
            await message.answer(text=text, reply_markup=keyboard)
        else:
            text = f'{TEXTS["left_class_start"]}{abs(class_left)}{TEXTS["left_class_no_paid"]}'
            await message.answer(text)
            await message.answer(TEXTS["payment"], reply_markup=futurium_tg_kb)
            await message.answer(TEXTS["thanks_after_pay"])
            await message.answer(TEXTS["finish"], reply_markup=finish_rkb_student)
        await state.set_state(Users.Student.state)
    else:
        await message.answer(text=TEXTS["no_name"])
        await message.answer(TEXTS["enter_name"], parse_mode="HTML")


# Handler for later pay
async def student_pay_later_thanks(message: Message, state: FSMContext):
    await message.answer(TEXTS["good"])
    await message.answer(TEXTS["finish"], reply_markup=finish_rkb_student)


# Handler for pay in advance
async def student_pay_in_advance(message: Message, state: FSMContext):
    await message.answer(TEXTS["payment"], reply_markup=futurium_tg_kb)
    await message.answer(TEXTS["thanks_after_pay"])
    await message.answer(TEXTS["finish"], reply_markup=finish_rkb_student)


# handler Студент > Хочу оплатити навчання
async def want_pay_hn(message: Message, state: FSMContext):
    kb = create_reply_kb(1, "individual", "in_pair", "group")
    await message.answer(TEXTS["want_pay_q1"], reply_markup=kb)


async def want_pay_indiv_hn(message: Message, state: FSMContext):
    price = get_price("individual")
    await message.answer(price)
    await message.answer(TEXTS["payment"], reply_markup=futurium_tg_kb)
    await message.answer(TEXTS["thanks_after_pay"])
    await message.answer(TEXTS["finish"], reply_markup=finish_rkb_student)


async def want_pay_in_pair_hn(message: Message, state: FSMContext):
    price = get_price("in_pair")
    await message.answer(price)
    await message.answer(TEXTS["payment"], reply_markup=futurium_tg_kb)
    await message.answer(TEXTS["thanks_after_pay"])
    await message.answer(TEXTS["finish"], reply_markup=finish_rkb_student)


async def want_pay_group_hn(message: Message, state: FSMContext):
    price = get_price("group")
    await message.answer(price)
    await message.answer(TEXTS["payment"], reply_markup=futurium_tg_kb)
    await message.answer(TEXTS["thanks_after_pay"])
    await message.answer(TEXTS["finish"], reply_markup=finish_rkb_student)


# Handler for review
async def student_send_review(message: Message, state: FSMContext):
    await message.answer(TEXTS["review_fill"], reply_markup=review_kb)
    await message.answer(TEXTS["review_thanks"])
    await message.answer(TEXTS["finish"], reply_markup=finish_rkb_student)


def register_student(dp: Dispatcher):
    dp.register_message_handler(student_start,
                                text=TEXTS["student"],
                                state="*")

    dp.register_message_handler(student_enter_name,
                                text=TEXTS["want_num_lesson"],
                                state=Users.Student)

    dp.register_message_handler(student_lessons_left,
                                regexp='[а-щА-ЩЬьЮюЯяЇїІіЄєҐґ]+\s+[а-щА-ЩЬьЮюЯяЇїІіЄєҐґ]',
                                state=Users.Student_name)

    dp.register_message_handler(student_pay_later_thanks,
                                text=TEXTS["later"],
                                state=Users.Student)

    dp.register_message_handler(student_pay_in_advance,
                                text=TEXTS["yes"],
                                state=Users.Student)

    dp.register_message_handler(want_pay_hn,
                                text=TEXTS["want_pay"],
                                state=Users.Student)

    dp.register_message_handler(want_pay_indiv_hn,
                                text=TEXTS["individual"],
                                state=Users.Student)

    dp.register_message_handler(want_pay_in_pair_hn,
                                text=TEXTS["in_pair"],
                                state=Users.Student)

    dp.register_message_handler(want_pay_group_hn,
                                text=TEXTS["group"],
                                state=Users.Student)

    dp.register_message_handler(student_send_review,
                                text=TEXTS["review"],
                                state=Users.Student)

    dp.register_message_handler(warning_not_name,
                                content_types='any',
                                state=Users.Student_name)
