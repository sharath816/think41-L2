from fastapi import FastAPI
from api.chat import chat_router

app = FastAPI(title="E-commerce Chatbot API")

app.include_router(chat_router, prefix="/api")
