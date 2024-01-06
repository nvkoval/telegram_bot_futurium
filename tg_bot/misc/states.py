from aiogram.fsm.state import State, StatesGroup


class Users(StatesGroup):
    Interested = State()
    Student = State()
    Student_name = State()
    Testing = State()
    Testing_in_progress = State()
