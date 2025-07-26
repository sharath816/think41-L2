from datetime import datetime
from typing import List, Literal
from pydantic import BaseModel

class Message(BaseModel):
    sender: Literal["user", "ai"]
    message: str
    timestamp: datetime

class Conversation(BaseModel):
    user_id: str
    started_at: datetime
    messages: List[Message]
