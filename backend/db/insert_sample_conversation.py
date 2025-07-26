from pymongo import MongoClient
from datetime import datetime, timezone

client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce_db"]

sample_convo = {
    "user_id": "u123",
    "started_at": datetime.now(timezone.utc),
    "messages": [
        {
            "sender": "user",
            "message": "What is my order status?",
            "timestamp": datetime.now(timezone.utc)
        },
        {
            "sender": "ai",
            "message": "Order ID 12345 is being shipped.",
            "timestamp": datetime.now(timezone.utc)
        }
    ]
}

db.conversations.insert_one(sample_convo)
print("✅ Sample conversation inserted.")
