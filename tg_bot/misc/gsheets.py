from aiogram.types import Message
from gspread_asyncio import AsyncioGspreadWorksheet, AsyncioGspreadClientManager


async def open_worksheet(google_client_manager: AsyncioGspreadClientManager,
                         sheet_name: str, worksheet_name: str) -> AsyncioGspreadWorksheet:
    google_client = await google_client_manager.authorize()
    sheet = await google_client.open(sheet_name)
    worksheet = await sheet.worksheet(worksheet_name)
    return worksheet


async def save_message(message: Message, col: int, worksheet_users: AsyncioGspreadWorksheet):
    cell = await worksheet_users.findall(str(message.from_user.id))
    await worksheet_users.update_cell(cell[-1].row, col, message.text)
    return


async def save_phone(message: Message, col: int, worksheet_users: AsyncioGspreadWorksheet):
    cell = await worksheet_users.findall(str(message.from_user.id))
    await worksheet_users.update_cell(cell[-1].row, col, message.contact.phone_number)
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
