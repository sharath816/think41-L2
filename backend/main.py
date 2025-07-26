from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.chat import chat_router

app = FastAPI()

# ✅ Add this block
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your React frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include API routes
app.include_router(chat_router, prefix="/api")
