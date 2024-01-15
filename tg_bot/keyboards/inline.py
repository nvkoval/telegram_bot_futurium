from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from json import dumps

from tg_bot.misc import texts


def create_inline_kb(width: int, *args: str) -> InlineKeyboardMarkup:
    inline_kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    for button in args:
        buttons.append(InlineKeyboardButton(
                        text=button,
                        callback_data=button))
    inline_kb_builder.row(*buttons, width=width)
    return inline_kb_builder.as_markup()


def create_inline_url_kb(text: str, url: str) -> InlineKeyboardMarkup:
    button = [
        [InlineKeyboardButton(text=text, url=url)]
        ]
    return InlineKeyboardMarkup(inline_keyboard=button)


futurium_tg_kb = create_inline_url_kb(
    text=texts.TEXT_LINK,
    url=texts.TG_LINK
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
