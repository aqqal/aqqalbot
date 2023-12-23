from fastapi import FastAPI
from app.auth import validate_token
# from app.routers.chats.router import router as chats_router
from app.routers.bots.router import router as bots_router

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Aqqalbot API Service",
    description="API service for Aqqal chatbot, Aqqalbot",
)

# app.include_router(chats_router)
app.include_router(bots_router)