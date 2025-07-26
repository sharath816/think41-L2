from datetime import datetime
from bson import ObjectId
from db.mongodb import get_collection
from schemas.chat import ChatRequest
import httpx
import os
from fastapi import HTTPException

collection = get_collection()

async def chat_with_bot(data: ChatRequest):
    try:
        # If conversation_id is provided, fetch it
        if data.conversation_id:
            try:
                conversation = await collection.find_one({"_id": ObjectId(data.conversation_id)})
                if not conversation:
                    raise HTTPException(status_code=404, detail="Conversation not found")
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid conversation_id")
        else:
            # Otherwise create a new conversation
            conversation = {
                "user_id": data.user_id,
                "messages": [],
                "created_at": datetime.utcnow()
            }
            result = await collection.insert_one(conversation)
            conversation["_id"] = result.inserted_id

        # Add user message to conversation
        user_message = {
            "role": "user",
            "content": data.message,
            "timestamp": datetime.utcnow()
        }
        conversation["messages"].append(user_message)

        # Query Groq LLM
        groq_api_key = os.getenv("GROQ_API_KEY")
        headers = {"Authorization": f"Bearer {groq_api_key}"}
        groq_url = "https://api.groq.com/openai/v1/chat/completions"

        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful customer support assistant."}
            ] + [
                {"role": m["role"], "content": m["content"]}
                for m in conversation["messages"]
            ],
            "temperature": 0.7
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(groq_url, headers=headers, json=payload)
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="LLM error")
            bot_reply = response.json()["choices"][0]["message"]["content"]

        # Add bot reply
        bot_message = {
            "role": "assistant",
            "content": bot_reply,
            "timestamp": datetime.utcnow()
        }
        conversation["messages"].append(bot_message)

        # Save updated conversation
        await collection.update_one(
            {"_id": conversation["_id"]},
            {"$set": {"messages": conversation["messages"]}}
        )

        return {
            "conversation_id": str(conversation["_id"]),
            "response": bot_reply
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
