from pydantic import BaseModel, Field
from datetime import datetime

class MessageCreate(BaseModel):
    user_message: str = Field(..., min_length=1, max_length=10000, description="The user's message, must be non-empty and up to 10000 characters.")

class MessageResponse(BaseModel):
    id: int
    user_message: str
    assistant_answer: str
    created_at: datetime
    answered_at: datetime

    class Config:
        from_attributes = True