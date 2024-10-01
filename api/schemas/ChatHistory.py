from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ChatHistoryBase(BaseModel):
    message: str
    sender: str
    step: str
    mce_id: int

class ChatHistoryCreate(ChatHistoryBase):
    pass

class ChatHistory(ChatHistoryBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
