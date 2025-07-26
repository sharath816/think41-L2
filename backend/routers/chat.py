from fastapi import APIRouter
from schemas.chat import ChatRequest
from controllers.chat import chat_with_bot

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(data: ChatRequest):
    return await chat_with_bot(data)
