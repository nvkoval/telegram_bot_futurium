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
    user = session.query(Users).filter(Users.id == user_id).first()
    return user
