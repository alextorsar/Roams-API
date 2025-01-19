from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    user_message: str
    
class MessageResponse(BaseModel):
    id: int
    user_message: str
    assistant_answer: str
    created_at: datetime
    answered_at: datetime
    class Config:
        from_attributes = True