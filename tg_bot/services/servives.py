from sqlalchemy.exc import IntegrityError

from tg_bot.models.models import Users
from tg_bot.db.database import session


def register_user(message):
    username = message.from_user.username if message.from_user.username else None
    user = Users(id=int(message.from_user.id), username=username)
    try:
        session.add(user)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()  # rollback session.add(user)
        return False


def select_user(user_id):
    user = session.query(Users.id, Users.name).filter(Users.id == user_id).first()
    return user

'''def register_user_full_name(message):
    user_full_name = message.text
    user = Users(id=int(message.from_user.id), name=user_full_name)
    try:
        session.add(user_full_name)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()  # rollback session.add(user)
        return False'''
