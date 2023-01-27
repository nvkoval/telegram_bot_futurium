from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tg_bot.texts.texts import TEXTS


def create_inline_kb(row_width: int, *args, **kwargs) -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardMarkup(row_width=row_width)
    if args:
        [inline_kb.insert(InlineKeyboardButton(
                            text=TEXTS[button],
                            callback_data=button)) for button in args]
    if kwargs:
        [inline_kb.insert(InlineKeyboardButton(
                            text=text,
                            callback_data=button)) for button, text in kwargs.items()]
    return inline_kb


finish_kb_student = create_inline_kb(1, "review", "want_pay", "want_num_lesson")
finish_kb_interested = create_inline_kb(1, "english_level", "format_education", "price")

payment_kb = InlineKeyboardMarkup()
button_payment = InlineKeyboardButton(text=TEXTS["text_link"], url=TEXTS["link"])
payment_kb.add(button_payment)

want_trial_more_kb = InlineKeyboardMarkup()
button_trial = InlineKeyboardButton(text=TEXTS["want_trial"], url=TEXTS["link"])
button_more = InlineKeyboardButton(text=TEXTS["want_more"], callback_data="want_more")
want_trial_more_kb.add(button_trial).add(button_more)
