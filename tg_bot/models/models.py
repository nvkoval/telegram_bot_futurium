from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from tg_bot.db.database import engine

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, default=None)
    fullname = Column(String, default=None)
    phone = Column(String, default=None)
    user_status = Column(String, default=None)
    is_admin = Column(Boolean, default=False)


# class UserStatus(Base):
#    __tablename__ = "user_status"
#    id = Column(Integer, primary_key=True)
#    type = Column(String)

Base.metadata.create_all(engine)
