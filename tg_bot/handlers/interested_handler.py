from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from tg_bot.keyboards.inline import create_inline_kb, finish_kb_interested
from tg_bot.texts.texts import TEXTS


# Hendler for answer if this is a people, who interested in styding
async def interested_start(callback: CallbackQuery):
    keyboard = create_inline_kb(1, "format_education", "price", "english_level")
    await callback.message.answer(text=TEXTS["interested_q1"], reply_markup=keyboard)
    await callback.answer()


async def price_photo(callback: CallbackQuery):
    with open('price.jpg', 'rb') as photo:
        await callback.message.answer_photo(photo)
        await callback.answer()
        await callback.message.answer(TEXTS["finish"], reply_markup=finish_kb_interested)


def register_interested_person(dp: Dispatcher):
    dp.register_callback_query_handler(interested_start, text="interested")
    dp.register_callback_query_handler(price_photo, text="price")
