from aiogram import Dispatcher, types


# Function for creating Menu button (the list of commands)
async def set_main_menu(dp: Dispatcher):
    main_menu_commands = [
        types.BotCommand(command='/start', description='Почніть спілкування  з ботом'),
        types.BotCommand(command='/contact', description='Contacts of Futurium English School'),
    ]
    await dp.bot.set_my_commands(main_menu_commands)
