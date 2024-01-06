from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from tg_bot.texts.texts import TEXTS


def create_reply_kb(width: int, *args: str) -> ReplyKeyboardMarkup:
    reply_kb_builder = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = []

    for button in args:
        buttons.append(
            KeyboardButton(text=TEXTS[button] if button in TEXTS else button)
        )

    reply_kb_builder.row(*buttons, width=width)
    return reply_kb_builder.as_markup(resize_keyboard=True,
                                      one_time_keyboard=True)


finish_rkb_student = create_reply_kb(1,
                                     "review",
                                     "want_pay",
                                     "want_num_lesson")


phone_button = KeyboardButton(text=TEXTS["phone"],
                              request_contact=True,
                              callback_data="thanks")
phone_rkb = ReplyKeyboardMarkup(
    keyboard=[[phone_button]],
    resize_keyboard=True,
    one_time_keyboard=True
)
