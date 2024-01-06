from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tg_bot.config import Config
from tg_bot.keyboards.inline import futurium_tg_kb, review_kb
from tg_bot.keyboards.reply import create_reply_kb, finish_rkb_student
from tg_bot.misc.gsheets import open_worksheet, num_class_left, get_price, save_message
from tg_bot.misc.states import Users
from tg_bot.texts.texts import TEXTS

student_router = Router()
student_router.message.filter(Users.Student)

student_name_router = Router()
student_name_router.message.filter(Users.Student_name)


# Handler for enter name
@student_router.message(F.text == TEXTS["want_num_lesson"])
async def student_enter_name(message: Message, state: FSMContext):
    await message.answer(TEXTS["enter_name"])
    await state.set_state(Users.Student_name.state)


# Handler for correct name and get a number of lessons
@student_name_router.message(F.text.regexp(r'[а-щА-ЩЬьЮюЯяЇїІіЄєҐґ]+\s+[а-щА-ЩЬьЮюЯяЇїІіЄєҐґ]'))
async def student_lessons_left(message: Message, state: FSMContext, config: Config):
    name = message.text
    google_client_manager = config.misc.google_client_manager
    sheet_name = config.misc.sheet_name
    worksheet_name = config.misc.worksheet_num
    worksheet_num = await open_worksheet(google_client_manager,
                                         sheet_name, worksheet_name)
    worksheet_num_col_values = await worksheet_num.col_values(2)
    if name in worksheet_num_col_values:
        worksheet_users = config.misc.worksheet_users
        worksheet_users = await open_worksheet(google_client_manager,
                                               sheet_name, worksheet_users)
        await save_message(message, 3, worksheet_users)

        class_left = int(await num_class_left(name, worksheet_num))
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
        await message.answer(TEXTS["enter_name"])


# Handler for incorrect name
@student_name_router.message()
async def warning_not_name(message: Message):
    await message.answer(text=TEXTS["enter_name_error"])


# Handler for later pay
@student_router.message(F.text == TEXTS["later"])
async def student_pay_later_thanks(message: Message):
    await message.answer(TEXTS["good"])
    await message.answer(TEXTS["finish"], reply_markup=finish_rkb_student)


# Handler for pay in advance
@student_router.message(F.text == TEXTS["yes"])
async def student_pay_in_advance(message: Message):
    await message.answer(TEXTS["payment"], reply_markup=futurium_tg_kb)
    await message.answer(TEXTS["thanks_after_pay"])
    await message.answer(TEXTS["finish"], reply_markup=finish_rkb_student)


# Handler for want to pay
@student_router.message(F.text == TEXTS["want_pay"])
async def student_want_pay(message: Message):
    kb = create_reply_kb(1, "individual", "in_pair", "group")
    await message.answer(TEXTS["want_pay_q1"], reply_markup=kb)


# Handler for individual payment
@student_router.message(F.text == TEXTS["individual"])
async def student_want_pay_indiv(message: Message, config: Config):
    google_client_manager = config.misc.google_client_manager
    sheet_name = config.misc.sheet_name
    worksheet_name = config.misc.worksheet_price
    worksheet_price = await open_worksheet(google_client_manager,
                                           sheet_name, worksheet_name)
    price = await get_price("individual", worksheet_price)
    await message.answer(price)
    await message.answer(TEXTS["payment"], reply_markup=futurium_tg_kb)
    await message.answer(TEXTS["thanks_after_pay"])
    await message.answer(TEXTS["finish"], reply_markup=finish_rkb_student)


# Handler for in pair payment
@student_router.message(F.text == TEXTS["in_pair"])
async def student_want_pay_in_pair(message: Message, config: Config):
    google_client_manager = config.misc.google_client_manager
    sheet_name = config.misc.sheet_name
    worksheet_name = config.misc.worksheet_price
    worksheet_price = await open_worksheet(google_client_manager,
                                           sheet_name, worksheet_name)
    price = await get_price("in_pair", worksheet_price)
    await message.answer(price)
    await message.answer(TEXTS["payment"], reply_markup=futurium_tg_kb)
    await message.answer(TEXTS["thanks_after_pay"])
    await message.answer(TEXTS["finish"], reply_markup=finish_rkb_student)


# Handler for group payment
@student_router.message(F.text == TEXTS["group"])
async def student_want_pay_group(message: Message, config: Config):
    google_client_manager = config.misc.google_client_manager
    sheet_name = config.misc.sheet_name
    worksheet_name = config.misc.worksheet_price
    worksheet_price = await open_worksheet(google_client_manager,
                                           sheet_name, worksheet_name)
    price = await get_price("group", worksheet_price)
    await message.answer(price)
    await message.answer(TEXTS["payment"], reply_markup=futurium_tg_kb)
    await message.answer(TEXTS["thanks_after_pay"])
    await message.answer(TEXTS["finish"], reply_markup=finish_rkb_student)


# Handler for review
@student_router.message(F.text == TEXTS["review"])
async def student_send_review(message: Message):
    await message.answer(TEXTS["review_fill"], reply_markup=review_kb)
    await message.answer(TEXTS["review_thanks"])
    await message.answer(TEXTS["finish"], reply_markup=finish_rkb_student)
