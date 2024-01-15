from aiogram import Bot
from aiogram.types import BotCommand

from tg_bot.misc.texts import TEXTS_MENU_COMMANDS


# Function for creating Menu button (the list of commands)
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in TEXTS_MENU_COMMANDS.items()
    ]
    await bot.set_my_commands(main_menu_commands)
