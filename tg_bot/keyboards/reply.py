from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from tg_bot.texts.texts import TEXTS


def create_reply_kb(row_width: int, *args) -> ReplyKeyboardMarkup:
    reply_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=True,
                                   row_width=row_width)
    for button in args:
        reply_kb.insert(KeyboardButton(text=TEXTS[button]))
    return reply_kb


want_trial_more_rkb = create_reply_kb(1, "want_trial", "want_more")


finish_rkb_student = create_reply_kb(1,
                                     "review",
                                     "want_pay",
                                     "want_num_lesson")

finish_rkb_interested = create_reply_kb(1,
                                        "english_level",
                                        "format_education",
                                        "price")


phone_rkb = ReplyKeyboardMarkup(row_width=1,
                                resize_keyboard=True,
                                one_time_keyboard=True)
phone_button = KeyboardButton(text=TEXTS["phone"], request_contact=True, callback_data="thanks")
phone_rkb.add(phone_button)
