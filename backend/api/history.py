from fastapi import APIRouter
from typing import List

chat_router = APIRouter()

@chat_router.get("/history/{session_id}")
async def get_history(session_id: str):
    # Dummy response or fetch from MongoDB later
    return {"messages": []}
