from datetime import datetime
from fastapi import HTTPException
from models.message import Message
from services.conversation import get_conversation_by_id
from sqlalchemy.orm import Session

def create_message(db: Session, user_message: str, conversation_id: int, user_id: int):
    created_at = datetime.now()
    conversation = get_conversation_by_id(db, conversation_id, user_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    assistant_answer = "I'm sorry, I can't understand your message"
    answered_at = datetime.now()
    new_message = Message(created_at=created_at, user_message=user_message, answered_at=answered_at, 
                          assistant_answer=assistant_answer, conversation_id=conversation_id)
    db.add(new_message)
    conversation.size += 1
    conversation.last_update = answered_at
    db.commit()
    db.refresh(new_message)
    db.refresh(conversation)
    return new_message

def get_messages_from_conversation_id(db: Session, conversation_id: int, user_id: int):
    conversation = get_conversation_by_id(db, conversation_id, user_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation.messages