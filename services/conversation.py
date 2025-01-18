from models.conversation import Conversation
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
    

def get_all_conversations_from_user(db: Session, user_id: int):
    return db.query(Conversation).filter(Conversation.user_id == user_id).all()

def get_conversation_by_id(db: Session, conversation_id: int, user_id: int):
    return db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == user_id).first()

def create_conversation(db: Session, title: str, user_id: int):
    new_conversation = Conversation(
        title=title,
        user_id=user_id
    )
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)
    return new_conversation