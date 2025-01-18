from fastapi import APIRouter, Depends, HTTPException
from core.dependencies import get_current_user_id
from schemas.conversation import ConversationResponse, ConversationCreate
from sqlalchemy.orm import Session
from database.database import get_db
from models.conversation import Conversation
from services.conversation import create_conversation, get_all_conversations_from_user, get_conversation_by_id

router = APIRouter()

@router.post("/", response_model=ConversationResponse, summary="Create a new conversation")
def register_conversation(new_conversation: ConversationCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """
        This endpoint is used to create a new conversation. It should receive a ConversationCreate schema with this fields:\n
        **title**: The title of the conversation\n
        It will return a ConversationResponse schema.\n
        This endpoint requires a valid JWT token in the header `Authorization`.
    """
    new_conversation = create_conversation(db, new_conversation.title, current_user_id)
    return new_conversation

@router.get("/", response_model=list[ConversationResponse], summary="Get all conversations")
def get_conversations(db: Session = Depends(get_db),current_user_id: int = Depends(get_current_user_id)):
    """
        This endpoint is used to get all conversations of the user logged in.\n
        It will return a list of ConversationResponse schema.\n
        This endpoint requires a valid JWT token in the header `Authorization`.
    """
    conversations = get_all_conversations_from_user(db, current_user_id)
    return conversations

@router.get("/{conversation_id}", response_model=ConversationResponse, summary="Get a conversation by id")
def get_conversation(conversation_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    """
        This endpoint is used to get a conversation by id.\n
        It will return a ConversationResponse schema.\n
        This endpoint requires a valid JWT token in the header `Authorization`.
    """
    conversation = get_conversation_by_id(db, conversation_id, current_user_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation