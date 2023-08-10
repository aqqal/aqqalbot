from fastapi import FastAPI
from app.auth import validate_token

app = FastAPI(
    title="Aqqalbot API Service",
    description="API service for Aqqal chatbot, Aqqalbot",
    dependencies=[Depends(validate_token)]
)