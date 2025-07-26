from fastapi import APIRouter, Request
from pydantic import BaseModel
from datetime import datetime, timezone
from pymongo import MongoClient
from bson import ObjectId
from fastapi import HTTPException
client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce_db"]

chat_router = APIRouter()

class ChatRequest(BaseModel):
    user_id: str
    message: str
    conversation_id: str | None = None

@chat_router.post("/chat")
def chat_endpoint(data: ChatRequest):
    user_message = {
        "sender": "user",
        "message": data.message,
        "timestamp": datetime.now(timezone.utc)
    }

    # Dummy AI response for now
    ai_response = {
        "sender": "ai",
        "message": "This is a placeholder response from the AI.",
        "timestamp": datetime.now(timezone.utc)
    }

    # If conversation_id not provided, start a new one
    if not data.conversation_id:
        new_convo = {
            "user_id": data.user_id,
            "started_at": datetime.now(timezone.utc),
            "messages": [user_message, ai_response]
        }
        inserted = db.conversations.insert_one(new_convo)
        return {
            "conversation_id": str(inserted.inserted_id),
            "response": ai_response["message"]
        }
    else:
        # Append to existing conversation
        db.conversations.update_one(
            {"_id": ObjectId(data.conversation_id)},
            {"$push": {"messages": {"$each": [user_message, ai_response]}}}
        )
        return {
            "conversation_id": data.conversation_id,
            "response": ai_response["message"]
        }
@chat_router.get("/history/{conversation_id}")
def get_conversation_history(conversation_id: str):
    try:
        obj_id = ObjectId(conversation_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid conversation ID")

    conversation = db.conversations.find_one({"_id": obj_id})
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return conversation["messages"]