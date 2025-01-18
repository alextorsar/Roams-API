from pydantic import BaseModel
from datetime import datetime

class ConversationCreate(BaseModel):
    title: str

class ConversationResponse(BaseModel):
    id: int
    title: str
    initial_timestamp: datetime
    last_update: datetime

    class Config:
        from_attributes = True 