from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from tg_bot.texts.texts import TEXTS


def create_reply_kb(row_width: int, *args) -> ReplyKeyboardMarkup:
    reply_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=True,
                                   row_width=row_width)
    for button in args:
        reply_kb.insert(KeyboardButton(text=TEXTS[button]))
    return reply_kb
