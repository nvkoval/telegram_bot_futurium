from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

from tg_bot.config import Config
from tg_bot.keyboards.inline import futurium_tg_kb
from tg_bot.keyboards.reply import create_reply_kb, phone_rkb
from tg_bot.misc.gsheets import open_worksheet, save_phone
from tg_bot.misc.states import Users
from tg_bot.misc import texts

interested_router = Router()
interested_router.message.filter(Users.Interested)

finish_rkb_interested = create_reply_kb(1, texts.ENGLISH_LEVEL,
                                        texts.FORMAT_EDUCATION,
                                        texts.PRICE)

want_trial_more_rkb = create_reply_kb(1, texts.WANT_TRIAL, texts.WANT_MORE)


@interested_router.message(F.text == texts.PRICE)
async def price_photo(message: Message):
    image_price = FSInputFile('price.jpg')
    await message.answer_photo(image_price)
    await message.answer(texts.FINISH,
                         reply_markup=finish_rkb_interested)


@interested_router.message(F.text == texts.FORMAT_EDUCATION)
async def type_of_study(message: Message):
    keyboard = create_reply_kb(1, texts.INDIVIDUAL, texts.IN_PAIR, texts.GROUP)
    await message.answer(texts.FORMAT_INTRO, reply_markup=keyboard)


@interested_router.message(F.text == texts.INDIVIDUAL)
async def individual_options(message: Message):
    await message.answer(texts.INDIVIDUAL_ANSWER, reply_markup=want_trial_more_rkb)


@interested_router.message(F.text == texts.IN_PAIR)
async def pair_options(message: Message):
    await message.answer(texts.IN_PAIR_ANSWER, reply_markup=want_trial_more_rkb)


@interested_router.message(F.text == texts.GROUP)
async def group_options(message: Message):
    await message.answer(texts.GROUP_ANSWER, reply_markup=want_trial_more_rkb)


@interested_router.message(F.text == texts.WANT_MORE)
async def send_phone_number(message: Message):
    await message.answer(texts.LEAVE_PHONE, reply_markup=phone_rkb)


@interested_router.message(F.contact)
async def phone_thanks(message: Message, config: Config):
    google_client_manager = config.misc.google_client_manager
    sheet_name = config.misc.sheet_name
    worksheet_users = config.misc.worksheet_users
    worksheet_users = await open_worksheet(google_client_manager,
                                           sheet_name, worksheet_users)
    await save_phone(message, 4, worksheet_users)
    await message.answer(texts.PHONE_THANKS, reply_markup=finish_rkb_interested)


@interested_router.message(F.text == texts.WANT_TRIAL)
async def want_trial(message: Message):
    await message.answer(texts.WANT_TRIAL_TEXT, reply_markup=futurium_tg_kb)
    await message.answer(texts.TRAIL_THANKS, reply_markup=finish_rkb_interested)


# Handler for english test
@interested_router.message(Users.Interested, F.text == texts.ENGLISH_LEVEL)
async def start_eng_test(message: Message, state: FSMContext):
    await message.answer(texts.TEST_HELLO)
    await state.set_state(Users.Testing.state)
