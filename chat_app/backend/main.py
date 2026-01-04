from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import os

# ------------------ App Init ------------------
app = FastAPI(title="Chat Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ Mongo Config ------------------
MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb://root:root@mongo:27017/chatdb?authSource=admin"
)

try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    print("✅ MongoDB connected")
except ServerSelectionTimeoutError as e:
    print("❌ MongoDB connection failed:", e)
    raise RuntimeError("MongoDB not reachable")

db = client.chatdb
messages = db.messages

# ------------------ Models ------------------
class Message(BaseModel):
    user: str
    text: str

# ------------------ HTTP APIs (Swagger) ------------------

@app.post("/messages")
def create_message(message: Message):
    """
    Use this API from Swagger to insert messages
    """
    messages.insert_one(message.dict())
    return {
        "status": "success",
        "message": message.dict()
    }


@app.get("/messages")
def get_messages():
    """
    Fetch all chat messages
    """
    result = []
    for m in messages.find({}, {"_id": 0}):
        result.append(m)
    return result

# ------------------ WebSocket (Frontend) ------------------

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_json()
            messages.insert_one(data)
            await ws.send_json(data)
    except Exception:
        await ws.close()
