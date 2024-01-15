from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from tg_bot.misc import texts


def create_reply_kb(width: int, *args: str) -> ReplyKeyboardMarkup:
    reply_kb_builder = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = []

    for button in args:
        buttons.append(
            KeyboardButton(text=button)
        )

    reply_kb_builder.row(*buttons, width=width)
    return reply_kb_builder.as_markup(resize_keyboard=True,
                                      one_time_keyboard=True)


phone_button = KeyboardButton(text=texts.PHONE,
                              request_contact=True,
                              callback_data=texts.PHONE_THANKS)
phone_rkb = ReplyKeyboardMarkup(
    keyboard=[[phone_button]],
    resize_keyboard=True,
    one_time_keyboard=True
)
