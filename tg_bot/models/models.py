from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from tg_bot.db.database import engine

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    name = Column(String)
    # phone = Column(String)
    # user_status_id = Column(Integer)
    admin = Column(Boolean, default=False)
    # student = Column(Boolean, default=None)


# class UserStatus(Base):
#    __tablename__ = "user_status"
#    id = Column(Integer, primary_key=True)
#    type = Column(String)

Base.metadata.create_all(engine)
