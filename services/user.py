from models.user import User
from sqlalchemy.orm import Session
from core.security import hash_password
from models.user import User


def get_user_by_id(user_id: int, db:Session) -> User:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(email: str, db:Session) -> User:
    return db.query(User).filter(User.email == email).first()

def create_new_user(password: str, name: str, email: str, db: Session) -> User:
    hashed_password = hash_password(password)
    new_user = User(name=name, email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user