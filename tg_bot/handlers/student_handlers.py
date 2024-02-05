from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tg_bot.config import Config
from tg_bot.keyboards.inline import create_inline_url_kb, futurium_tg_kb
from tg_bot.keyboards.reply import create_reply_kb
from tg_bot.misc import texts
from tg_bot.misc.gsheets import open_worksheet, num_class_left, get_price, save_message
from tg_bot.misc.states import Users


student_router = Router()
student_router.message.filter(Users.Student)

student_name_router = Router()
student_name_router.message.filter(Users.Student_name)

finish_rkb_student = create_reply_kb(1, texts.REVIEW,
                                     texts.WANT_PAY,
                                     texts.WANT_NUM_LESSONS)


# Handler for enter name
@student_router.message(F.text == texts.WANT_NUM_LESSONS)
async def student_enter_name(message: Message, state: FSMContext):
    await message.answer(texts.ENTER_NAME)
    await state.set_state(Users.Student_name.state)


# Handler for correct name and get a number of lessons
@student_name_router.message(F.text.regexp(r"[а-щА-ЩЬьЮюЯяЇїІіЄєҐґ]+\s+[а-щА-ЩЬьЮюЯяЇїІіЄєҐґ]"))
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
        await save_message(message, 5, worksheet_users)

        class_left = int(await num_class_left(name, worksheet_num))
        keyboard = create_reply_kb(1, texts.YES, texts.LATER)
        if class_left >= 0:
            text = f"{texts.LEFT_CLASS_START}{class_left}{texts.LEFT_CLASS_PAID}"
            await message.answer(text=text, reply_markup=keyboard)
        else:
            text = f"{texts.LEFT_CLASS_START}{abs(class_left)}{texts.LEFT_CLASS_NO_PAID}"
            await message.answer(f"{text}\n{texts.PAYMENT}", reply_markup=futurium_tg_kb)
            await message.answer(texts.THANKS_AFTER_PAY, reply_markup=finish_rkb_student)
        await state.set_state(Users.Student.state)
    else:
        await message.answer(text=texts.NO_NAME)
        await message.answer(texts.ENTER_NAME)


# Handler for incorrect name
@student_name_router.message(~Command(commands="cancel"))
async def warning_not_name(message: Message):
    await message.answer(text=texts.ENTER_NAME_ERROR)


# Handler for later pay
@student_router.message(F.text == texts.LATER)
async def student_pay_later_thanks(message: Message):
    await message.answer(texts.GOOD, reply_markup=finish_rkb_student)


# Handler for pay in advance
@student_router.message(F.text == texts.YES)
async def student_pay_in_advance(message: Message):
    await message.answer(texts.PAYMENT, reply_markup=futurium_tg_kb)
    await message.answer(texts.THANKS_AFTER_PAY, reply_markup=finish_rkb_student)


# Handler for want to pay
@student_router.message(F.text == texts.WANT_PAY)
async def student_want_pay(message: Message):
    keyboard = create_reply_kb(1, texts.INDIVIDUAL, texts.IN_PAIR, texts.GROUP)
    await message.answer(texts.WANT_PAY_Q1, reply_markup=keyboard)


# Handler for individual payment
@student_router.message(F.text == texts.INDIVIDUAL)
async def student_want_pay_indiv(message: Message, config: Config):
    google_client_manager = config.misc.google_client_manager
    sheet_name = config.misc.sheet_name
    worksheet_name = config.misc.worksheet_price
    worksheet_price = await open_worksheet(google_client_manager,
                                           sheet_name, worksheet_name)
    price = await get_price("individual", worksheet_price)
    await message.answer(f"{price}\n{texts.PAYMENT}", reply_markup=futurium_tg_kb)
    await message.answer(texts.THANKS_AFTER_PAY, reply_markup=finish_rkb_student)


# Handler for in pair payment
@student_router.message(F.text == texts.IN_PAIR)
async def student_want_pay_in_pair(message: Message, config: Config):
    google_client_manager = config.misc.google_client_manager
    sheet_name = config.misc.sheet_name
    worksheet_name = config.misc.worksheet_price
    worksheet_price = await open_worksheet(google_client_manager,
                                           sheet_name, worksheet_name)
    price = await get_price("in_pair", worksheet_price)
    await message.answer(price)
    await message.answer(texts.PAYMENT, reply_markup=futurium_tg_kb)
    await message.answer(texts.THANKS_AFTER_PAY, reply_markup=finish_rkb_student)


# Handler for group payment
@student_router.message(F.text == texts.GROUP)
async def student_want_pay_group(message: Message, config: Config):
    google_client_manager = config.misc.google_client_manager
    sheet_name = config.misc.sheet_name
    worksheet_name = config.misc.worksheet_price
    worksheet_price = await open_worksheet(google_client_manager,
                                           sheet_name, worksheet_name)
    price = await get_price("group", worksheet_price)
    await message.answer(price)
    await message.answer(texts.PAYMENT, reply_markup=futurium_tg_kb)
    await message.answer(texts.THANKS_AFTER_PAY, reply_markup=finish_rkb_student)


# Handler for review
@student_router.message(F.text == texts.REVIEW)
async def student_send_review(message: Message):
    review_kb = create_inline_url_kb(
        text=texts.FORM_REVIEW_TEXT,
        url=texts.FORM_REVIEW_URL
    )
    await message.answer(texts.REVIEW_FILL, reply_markup=review_kb)
    await message.answer(texts.REVIEW_THANKS, reply_markup=finish_rkb_student)
