import gspread
from aiogram.types import Message
from tg_bot.services.servives import select_user
from tg_bot.models.models import Users

# Authentication to interact with the Google Drive API
gc = gspread.service_account("tgbot_futurium.json")
sheet = gc.open("Futurium_price")
worksheet_num = sheet.worksheet("num_classes")
worksheet_users = sheet.worksheet("users_from_bot")
worksheet_price = sheet.worksheet("price")


def num_class_left(name: str) -> str:
    cell = worksheet_num.find(name)
    num_class_left = worksheet_num.cell(cell.row, 5).value
    return num_class_left

#  find me the first empty row in specific column
def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)


def save_user(user: Users):
    next_row = next_available_row(worksheet_users)
    if str(user.id) not in worksheet_users.col_values(1):
        worksheet_users.update_cell(next_row, 1, user.id)
        worksheet_users.update_cell(next_row, 2, user.username)
    return


def save_user_full_name(message: Message):
    cell = worksheet_users.find(str(message.from_user.id))
    if worksheet_users.cell(cell.row, 3).value is None:
        worksheet_users.update_cell(cell.row, 3, message.text)
    return


def get_price(option: str) -> str:
    d = {
        "individual": 2,
        "in_pair": 3,
        "group": 4,
    }
    price = worksheet_price.cell(d[option], 2).value
    return str(price)+" грн"
