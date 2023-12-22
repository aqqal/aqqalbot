from fastapi import APIRouter, Depends
from app.auth import validate_token

from bot.openai import new_bot

from app.routers.bots.models import (
	NewBotRequest,
	UpdateBotRequest,
	GetBotsResponse
)

import time

router = APIRouter(
    prefix="/bots",
    dependencies=[Depends(validate_token)]
)

@router.post("", response_model= Bot)
def new_bot(body: NewBotRequest):
	"""
	Creates a new bot

	"""
	
	bot = await new_bot(body.model_id, body.prompt, body.name)
	return bot 

@router.get("", response_model=GetBotsResponse)
def get_bots():
	pass


@router.patch("/{id}", response_model=NewBotResponse)
def update_bot(id: str, body: UpdateBotRequest):
	pass

@router.get("/defaults", response_model=NewBotResponse)
def get_default_bot():
	pass

@router.patch("/defaults")
def set_default_bot():
	pass
