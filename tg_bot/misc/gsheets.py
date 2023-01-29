import gspread
from aiogram.types import Message
from gspread import Worksheet


# Authentication to interact with the Google Drive API
gc = gspread.service_account("tgbot_futurium.json")
sheet = gc.open("Futurium_price")


worksheet_num = sheet.worksheet("num_classes")
worksheet_users = sheet.worksheet("users_from_bot")
worksheet_price = sheet.worksheet("price")
worksheet_test = sheet.worksheet("test_result")


def num_class_left(name: str) -> str:
    cell = worksheet_num.find(name)
    num_class_left = worksheet_num.cell(cell.row, 5).value
    return num_class_left


#  find me the first empty row in specific column
def next_available_row(worksheet: Worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)


def save_user(message: Message):
    username = message.from_user.username if message.from_user.username else None
    id = message.from_user.id
    next_row = next_available_row(worksheet_users)
    if str(message.from_user.id) not in worksheet_users.col_values(1):
        worksheet_users.update_cell(next_row, 1, id)
        worksheet_users.update_cell(next_row, 2, username)
    return


def save_message(message: Message, col: int):
    cell = worksheet_users.find(str(message.from_user.id))
    if worksheet_users.cell(cell.row, col).value is None:
        worksheet_users.update_cell(cell.row, col, message.text)
    return


def save_user_status(message: Message, col: int):
    cell = worksheet_users.find(str(message.from_user.id))
    worksheet_users.update_cell(cell.row, col, message.text)
    return


def get_price(option: str) -> str:
    d = {
        "individual": 2,
        "in_pair": 3,
        "group": 4,
    }
    price = worksheet_price.cell(d[option], 2).value
    return str(price)+" грн"


def save_phone(message: Message, col: int):
    cell = worksheet_users.find(str(message.from_user.id))
    if worksheet_users.cell(cell.row, col).value is None:
        worksheet_users.update_cell(cell.row, col, message.contact["phone_number"])
    return


# Adding result of test to table
def adding_info_spreadsheet(user):
    rows = worksheet_test.get_all_values()
    counter = 1
    for row in rows:
        counter += 1
    worksheet_test.update_cell(counter, 1, user[0])
    worksheet_test.update_cell(counter, 2, user[1])
    worksheet_test.update_cell(counter, 3, user[2])
    worksheet_test.update_cell(counter, 4, user[3])
