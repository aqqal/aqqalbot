from fastapi import FastAPI
import uvicorn

from auth import validate_token
from routers.chats.router import router as chats_router
from routers.bots.router import router as bots_router

from logger import logger
from config import log_config

app = FastAPI(
    title="Aqqalbot API Service",
    description="API service for Aqqal chatbot, Aqqalbot",
)

app.include_router(chats_router)
app.include_router(bots_router)

uvicorn.run(app, log_config=log_config, port=80, host="0.0.0.0")