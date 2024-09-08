from sqlalchemy.orm import Session

from auth import get_password_hash
from models import User, Message
from schemas import UserCreate


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_message(db: Session, text: str, response: str, owner_id: int):
    db_message = Message(text=text, response=response, owner_id=owner_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_messages_by_user(db: Session, user_id: int):
    return db.query(Message).filter(Message.owner_id == user_id).all()
