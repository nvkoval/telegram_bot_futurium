from aiogram.types import Message
from dataclasses import dataclass
from gspread_asyncio import AsyncioGspreadWorksheet, AsyncioGspreadClientManager


async def open_worksheet(google_client_manager: AsyncioGspreadClientManager,
                         sheet_name: str, worksheet_name: str) -> AsyncioGspreadWorksheet:
    google_client = await google_client_manager.authorize()
    sheet = await google_client.open(sheet_name)
    worksheet = await sheet.worksheet(worksheet_name)
    return worksheet


#  find me the first empty row in specific column
async def next_available_row(worksheet: AsyncioGspreadWorksheet) -> str:
    str_list = list(filter(None, await worksheet.col_values(1)))
    return str(len(str_list)+1)


async def save_user(message: Message, worksheet_users: AsyncioGspreadWorksheet):
    username = message.from_user.username if message.from_user.username else None
    id = message.from_user.id
    next_row = await next_available_row(worksheet_users)
    if str(message.from_user.id) not in await worksheet_users.col_values(1):
        await worksheet_users.update_cell(next_row, 1, id)
        await worksheet_users.update_cell(next_row, 2, username)
    return


async def save_message(message: Message, col: int, worksheet_users: AsyncioGspreadWorksheet):
    cell = await worksheet_users.find(str(message.from_user.id))
    cell_value = await worksheet_users.cell(cell.row, col)
    if cell_value.value is None:
        await worksheet_users.update_cell(cell.row, col, message.text)
    return


async def save_user_status(message: Message, col: int, worksheet_users: AsyncioGspreadWorksheet):
    cell = await worksheet_users.find(str(message.from_user.id))
    await worksheet_users.update_cell(cell.row, col, message.text)
    return


async def save_phone(message: Message, col: int, worksheet_users: AsyncioGspreadWorksheet):
    cell = await worksheet_users.find(str(message.from_user.id))
    cell_value = await worksheet_users.cell(cell.row, col)
    if cell_value.value is None:
        await worksheet_users.update_cell(cell.row, col, message.contact.phone_number)
    return


async def num_class_left(name: str, worksheet_num: AsyncioGspreadWorksheet) -> str:
    cell = await worksheet_num.find(name)
    num_class_left = await worksheet_num.cell(cell.row, 5)
    return num_class_left.value


async def get_price(option: str, worksheet_price: AsyncioGspreadWorksheet) -> str:
    d = {
        "individual": 2,
        "in_pair": 3,
        "group": 4,
    }
    price = await worksheet_price.cell(d[option], 2)
    return str(price.value)+" грн"


@dataclass
class GoogleForm_test_result:
    first_name: str
    last_name: str
    username: str
    correct_answers: int
    date: str

    COLUMNS = ["first_name", "last_name", "username", "correct_answers", "date"]

    def create_row(self):
        return [
            str(getattr(self, row_name, '') or '')
            for row_name in self.COLUMNS
        ]


# Adding result of test to table
async def adding_info_to_sheet(worksheet_test: AsyncioGspreadWorksheet,
                               GoogleForm_test_result: GoogleForm_test_result):
    await worksheet_test.append_row(GoogleForm_test_result.create_row())
