import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from tg_bot.config import load_config

config = load_config(".env")

DATABASE_URI = "postgresql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(
    DATABASE_URI.format(
        user=config.db.user,
        password=config.db.password,
        host=config.db.host,
        port=5432,
        database=config.db.database,
        )
)

# Create database if it does not exist.
if not database_exists(engine.url):
    create_database(engine.url)
else:
    # Connect the database if exists.
    engine.connect()

Session = sessionmaker(bind=engine)

session = Session()
