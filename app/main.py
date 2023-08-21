from fastapi import FastAPI
from app.auth import validate_token
from routes.chats.router import router as chats_router

app = FastAPI(
    title="Aqqalbot API Service",
    description="API service for Aqqal chatbot, Aqqalbot",
)

app.include_router(chats_router)