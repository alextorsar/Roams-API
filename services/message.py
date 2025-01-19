from datetime import datetime
from fastapi import HTTPException
from models.message import Message
from models.conversation import Conversation
from services.conversation import get_conversation_by_id, update_conversation_size_and_last_update, update_conversation_summary
from services.llm import get_initial_response, get_response_with_user_message_and_all_previous_messages, get_response_with_summary_and_recent_messages, get_summary_of_complete_conversation, get_accumulated_summary_of_conversation
from sqlalchemy.orm import Session

def create_message(db: Session, user_message: str, conversation_id: int, user_id: int):
    created_at = datetime.now()
    conversation = get_conversation_by_id(db, conversation_id, user_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    try:
        summary = None
        assistant_answer = get_LLM_response(conversation, user_message)
    except Exception as e:
        raise e
    answered_at = datetime.now()
    if type(assistant_answer) == tuple:
        assistant_answer, summary = assistant_answer
    new_message = Message(created_at=created_at, user_message=user_message, answered_at=answered_at, 
                        assistant_answer=assistant_answer, conversation_id=conversation_id)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    update_conversation_size_and_last_update(db, conversation, answered_at)
    if summary:
        update_conversation_summary(db, conversation, summary)
    return new_message

def get_messages_from_conversation_id(db: Session, conversation_id: int, user_id: int):
    conversation = get_conversation_by_id(db, conversation_id, user_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation.messages

def get_LLM_response(conversation:Conversation, user_message:str):
    try:
        if conversation.size == 0:
            response = get_initial_response(user_message)
        elif conversation.size <= 10:
            response = get_response_with_user_message_and_all_previous_messages(user_message, conversation)
        elif conversation.size <= 50:
            summary = get_summary_of_complete_conversation(conversation)
            response = get_response_with_summary_and_recent_messages(user_message, conversation, summary)
            response = (response, summary)
        else:
            accumulated_summary = get_accumulated_summary_of_conversation(conversation)
            response = get_response_with_summary_and_recent_messages(user_message, conversation, accumulated_summary)
            response = (response, accumulated_summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error in LLM response")
    return response