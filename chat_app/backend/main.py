
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb://root:root@mongo:27017/chatdb?authSource=admin"
)
client = MongoClient(MONGO_URL)

# client = MongoClient("mongodb://mongo:27017")
db = client.chatdb
messages = db.messages

@app.get("/messages")
def get_messages():
    return [{"user": m["user"], "text": m["text"]} for m in messages.find()]

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        data = await ws.receive_json()
        messages.insert_one(data)
        await ws.send_json(data)
