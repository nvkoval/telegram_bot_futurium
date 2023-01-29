from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, Message, ReplyKeyboardRemove

from tg_bot.keyboards.inline import futurium_tg_kb
from tg_bot.keyboards.reply import create_reply_kb, finish_rkb_interested
from tg_bot.keyboards.reply import phone_rkb, want_trial_more_rkb
from tg_bot.misc.gsheets import save_phone, save_user_status
from tg_bot.misc.states import Users
from tg_bot.texts.texts import TEXTS



# Handler for answer if this is a people, who interested in styding
async def interested_start(message: Message, state: FSMContext):
    save_user_status(message, 5)
    keyboard = create_reply_kb(1, "format_education", "price", "english_level")
    await message.answer(text=TEXTS["interested_q1"], reply_markup=keyboard)
    await state.set_state(Users.Interested.state)


async def price_photo(message: Message, state: FSMContext):
    with open('price.jpg', 'rb') as photo:
        await message.answer_photo(photo)
        await message.answer(TEXTS["finish"],
                             reply_markup=finish_rkb_interested)


async def type_of_study(message: Message, state: FSMContext):
    keyboard = create_reply_kb(1, "individual", "in_pair", "group")
    await message.answer(TEXTS["format_intro"], reply_markup=keyboard)


async def individual_options(message: Message, state: FSMContext):
    await message.answer(TEXTS["individual_answer"], reply_markup=want_trial_more_rkb)


async def pair_options(message: Message, state: FSMContext):
    await message.answer(TEXTS["in_pair_answer"], reply_markup=want_trial_more_rkb)


async def group_options(message: Message, state: FSMContext):
    await message.answer(TEXTS["group_answer"], reply_markup=want_trial_more_rkb)


async def send_phone_number(message: Message, state: FSMContext):
    await message.answer(TEXTS["leave_phone"], reply_markup=phone_rkb)


async def phone_thanks(message: Message, state: FSMContext):
    save_phone(message, 4)
    await message.answer(TEXTS["phone_thanks"], reply_markup=ReplyKeyboardRemove())
    await message.answer(TEXTS["finish"], reply_markup=finish_rkb_interested)


async def want_trial(message: Message, state: FSMContext):
    await message.answer(TEXTS["want_trail_text"], reply_markup=futurium_tg_kb)
    await message.answer(TEXTS["trail_thanks"], reply_markup=ReplyKeyboardRemove())
    await message.answer(TEXTS["finish"], reply_markup=finish_rkb_interested)


def register_interested_person(dp: Dispatcher):
    dp.register_message_handler(interested_start,
                                text=TEXTS["interested"],
                                state="*")

    dp.register_message_handler(price_photo,
                                text=TEXTS["price"],
                                state=Users.Interested)

    dp.register_message_handler(type_of_study,
                                text=TEXTS["format_education"],
                                state=Users.Interested)

    dp.register_message_handler(individual_options,
                                text=TEXTS["individual"],
                                state=Users.Interested)

    dp.register_message_handler(pair_options,
                                text=TEXTS["in_pair"],
                                state=Users.Interested)

    dp.register_message_handler(group_options,
                                text=TEXTS["group"],
                                state=Users.Interested)

    dp.register_message_handler(send_phone_number,
                                text=TEXTS["want_more"],
                                state=Users.Interested)

    dp.register_message_handler(phone_thanks,
                                content_types=ContentType.CONTACT,
                                state=Users.Interested)

    dp.register_message_handler(want_trial,
                                text=TEXTS["want_trial"],
                                state=Users.Interested)
