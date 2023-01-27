from aiogram.dispatcher.filters.state import State, StatesGroup

class Users(StatesGroup):
    Student = State()
    Interested = State()
