from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from json import dumps

from tg_bot.texts.texts import TEXTS


def create_inline_kb(width: int, *args: str) -> InlineKeyboardMarkup:
    inline_kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    for button in args:
        buttons.append(InlineKeyboardButton(
                        text=TEXTS[button] if button in TEXTS else button,
                        callback_data=button))
    inline_kb_builder.row(*buttons, width=width)
    return inline_kb_builder.as_markup()


finish_kb_student = create_inline_kb(1,
                                     "review",
                                     "want_pay",
                                     "want_num_lesson")

finish_kb_interested = create_inline_kb(1,
                                        "english_level",
                                        "format_education",
                                        "price")


def create_inline_url_kb(text: str, url: str) -> InlineKeyboardMarkup:
    button = [
        [InlineKeyboardButton(text=text, url=url)]
        ]
    return InlineKeyboardMarkup(inline_keyboard=button)


futurium_tg_kb = create_inline_url_kb(
    text=TEXTS["text_link"],
    url=TEXTS["link"]
)

contact_url_kb = create_inline_url_kb(
    text=TEXTS["contact_url"],
    url=TEXTS["url"]
)

review_kb = create_inline_url_kb(
    text=TEXTS["form_review_text"],
    url=TEXTS["form_review_url"]
)


button_trial = InlineKeyboardButton(text=TEXTS["want_trial"],
                                    url=TEXTS["link"])
button_more = InlineKeyboardButton(text=TEXTS["want_more"],
                                   callback_data="want_more")
want_trial_more_kb = InlineKeyboardMarkup(
    inline_keyboard=[[button_trial],
                     [button_more]]
)


def compose_keyboard_for_test(questions: list, question: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    for i in range(len(questions[question]["variants"])):
        cd = {
            "question": question,
            "answer": i
        }
        buttons.append(InlineKeyboardButton(
                        text=questions[question]["variants"][i],
                        callback_data=dumps(cd)))
    keyboard.row(*buttons)
    return keyboard.as_markup()
