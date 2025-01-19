from fastapi import APIRouter, Depends
from typing import List
from schemas.message import MessageResponse, MessageCreate
from sqlalchemy.orm import Session
from database.database import get_db
from services.message import create_message, get_messages_from_conversation_id
from core.dependencies import get_current_user_id


router = APIRouter()

@router.post("/conversation/{conversation_id}", response_model=MessageResponse, summary="Create a new message in a conversation")
def create_message_in_conversation(conversation_id: int, new_message: MessageCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """
        This endpoint is used to create a new message in a conversation. It should receive a MessageCreate schema with this fields:\n
        **user_message**: The content of the message\n
        It will return a MessageResponse schema.\n
        This endpoint requires a valid JWT token in the header `Authorization`.
    """
    new_message = create_message(db, new_message.user_message, conversation_id, current_user_id)
    return new_message

@router.get("/conversation/{conversation_id}", response_model=List[MessageResponse], summary="Get all messages in a conversation")
def get_messages_from_conversation(conversation_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """
        This endpoint is used to get all messages in a conversation. It will return a list of MessageResponse schema.\n
        This endpoint requires a valid JWT token in the header `Authorization`.
    """
    messages = get_messages_from_conversation_id(db, conversation_id, current_user_id)
    return messages

