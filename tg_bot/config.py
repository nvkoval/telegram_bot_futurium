from dataclasses import dataclass
from environs import Env
from google.oauth2.service_account import Credentials
from gspread_asyncio import AsyncioGspreadClientManager


def get_scoped_credentials(credentials, scopes):
    def prepare_credentials():
        return credentials.with_scopes(scopes)

    return prepare_credentials


@dataclass
class TgBot:
    token: str
    use_redis: bool

    @staticmethod
    def from_env(env: Env):
        token = env.str("BOT_TOKEN")
        use_redis = env.bool("USE_REDIS")
        return TgBot(token=token, use_redis=use_redis)


@dataclass
class Miscellaneous:
    google_client_manager: AsyncioGspreadClientManager
    sheet_name: str
    worksheet_num: str
    worksheet_users: str
    worksheet_price: str
    worksheet_test: str

    @staticmethod
    def from_env(env: Env, google_client_manager: AsyncioGspreadClientManager):
        google_client_manager = google_client_manager
        sheet_name = env.str("SHEET_NAME")
        worksheet_num = env.str("WORKSHEET_NUM")
        worksheet_users = env.str("WORKSHEET_USERS")
        worksheet_price = env.str("WORKSHEET_PRICE")
        worksheet_test = env.str("WORKSHEET_TEST")
        return Miscellaneous(
            google_client_manager=google_client_manager,
            sheet_name=sheet_name,
            worksheet_num=worksheet_num,
            worksheet_users=worksheet_users,
            worksheet_price=worksheet_price,
            worksheet_test=worksheet_test
        )


@dataclass
class Config:
    tg_bot: TgBot
    misc: Miscellaneous


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]

    google_credentials = Credentials.from_service_account_file("config_google.json")
    scoped_credentials = get_scoped_credentials(google_credentials, scopes)
    google_client_manager = AsyncioGspreadClientManager(scoped_credentials)

    return Config(
        tg_bot=TgBot.from_env(env),
        misc=Miscellaneous.from_env(env, google_client_manager)
    )
