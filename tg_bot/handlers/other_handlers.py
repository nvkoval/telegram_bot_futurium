from aiogram import Dispatcher
from aiogram.types import Message, ContentType
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tg_bot.texts.texts import TEXTS


# Handler for /contact command
async def contact_command(message: Message):
    text = TEXTS["contact"]
    text_url = TEXTS["contact_url"]
    url = TEXTS["url"]
    keyboard_url = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text=text_url, url=url)
    keyboard_url.add(button)
    await message.answer(text, reply_markup=keyboard_url)


async def unknown_text(message: Message):
    await message.answer(TEXTS["unknown_text"])


def register_contact_command(dp: Dispatcher):
    dp.register_message_handler(contact_command, commands="contact")


def register_unknown_text(dp: Dispatcher):
    dp.register_message_handler(unknown_text, content_types=ContentType.ANY)
