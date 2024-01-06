from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message, ReplyKeyboardRemove

from tg_bot.config import Config
from tg_bot.keyboards.inline import futurium_tg_kb
from tg_bot.keyboards.reply import create_reply_kb, phone_rkb
from tg_bot.misc.gsheets import open_worksheet, save_phone
from tg_bot.misc.states import Users
from tg_bot.texts.texts import TEXTS

interested_router = Router()
interested_router.message.filter(Users.Interested)

finish_rkb_interested = create_reply_kb(1,
                                        "english_level",
                                        "format_education",
                                        "price")

want_trial_more_rkb = create_reply_kb(1, "want_trial", "want_more")


@interested_router.message(F.text == TEXTS["price"])
async def price_photo(message: Message):
    image_price = FSInputFile('price.jpg')
    await message.answer_photo(image_price)
    await message.answer(TEXTS["finish"],
                         reply_markup=finish_rkb_interested)


@interested_router.message(F.text == TEXTS["format_education"])
async def type_of_study(message: Message):
    keyboard = create_reply_kb(1, "individual", "in_pair", "group")
    await message.answer(TEXTS["format_intro"], reply_markup=keyboard)


@interested_router.message(F.text == TEXTS["individual"])
async def individual_options(message: Message):
    await message.answer(TEXTS["individual_answer"], reply_markup=want_trial_more_rkb)


@interested_router.message(F.text == TEXTS["in_pair"])
async def pair_options(message: Message):
    await message.answer(TEXTS["in_pair_answer"], reply_markup=want_trial_more_rkb)


@interested_router.message(F.text == TEXTS["group"])
async def group_options(message: Message):
    await message.answer(TEXTS["group_answer"], reply_markup=want_trial_more_rkb)


@interested_router.message(F.text == TEXTS["want_more"])
async def send_phone_number(message: Message):
    await message.answer(TEXTS["leave_phone"], reply_markup=phone_rkb)


@interested_router.message(F.contact)
async def phone_thanks(message: Message, config: Config):
    google_client_manager = config.misc.google_client_manager
    sheet_name = config.misc.sheet_name
    worksheet_users = config.misc.worksheet_users
    worksheet_users = await open_worksheet(google_client_manager,
                                           sheet_name, worksheet_users)
    await save_phone(message, 4, worksheet_users)
    await message.answer(TEXTS["phone_thanks"], reply_markup=ReplyKeyboardRemove())
    await message.answer(TEXTS["finish"], reply_markup=finish_rkb_interested)


@interested_router.message(F.text == TEXTS["want_trial"])
async def want_trial(message: Message):
    await message.answer(TEXTS["want_trail_text"], reply_markup=futurium_tg_kb)
    await message.answer(TEXTS["trail_thanks"], reply_markup=ReplyKeyboardRemove())
    await message.answer(TEXTS["finish"], reply_markup=finish_rkb_interested)


# Handler for english test
@interested_router.message(Users.Interested, F.text == TEXTS["english_level"])
async def start_eng_test(message: Message, state: FSMContext):
    await message.answer(TEXTS["test_hello"])
    await state.set_state(Users.Testing.state)
