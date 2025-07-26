from fastapi import APIRouter, Request
from models.chat import ChatRequest, ChatResponse
from db.mongodb import get_database
from bson import ObjectId
from services.groq import get_groq_response  # ✅ Import Groq service

router = APIRouter()
db = get_database()

@router.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # 1. Get Groq response
    ai_response = await get_groq_response(request.message)

    # 2. Create a conversation if new
    conversation_id = request.conversation_id
    if not conversation_id:
        result = await db.conversations.insert_one({
            "user_id": request.user_id,
            "messages": []
        })
        conversation_id = str(result.inserted_id)

    # 3. Update the conversation history
    await db.conversations.update_one(
        {"_id": ObjectId(conversation_id)},
        {
            "$push": {
                "messages": {
                    "user": request.message,
                    "bot": ai_response
                }
            }
        }
    )

    # 4. Return response
    return ChatResponse(conversation_id=conversation_id, response=ai_response)
