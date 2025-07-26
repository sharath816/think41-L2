# models/chat.py

from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    conversation_id: str
    response: str
