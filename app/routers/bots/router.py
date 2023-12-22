from fastapi import APIRouter, Depends
from app.auth import validate_token
from typing import List

from app.routers.bots.models import (
	NewBotRequest,
	UpdateBotRequest,
)

from datastore.botstore_json import (
	get_default_bot,
	list_bots,
	save_bot
)

from bot.openai import new_bot
from models.bot import Bot

import time

router = APIRouter(
    prefix="/bots",
    dependencies=[Depends(validate_token)]
)

@router.post("", response_model=Bot)
async def new_bot(body: NewBotRequest):
	"""
	Creates a new bot
	"""
	
	bot = await new_bot(body.model_id, body.prompt, body.name)
	await save_bot(bot)

	return bot 

@router.get("", response_model=List[Bot])
async def get_bots():
	"""
	Returns a list of all bots
	"""

	return list_bots()	


@router.patch("/{id}", response_model=Bot)
async def update_bot(id: str, body: UpdateBotRequest):
	"""
	Updates a bot by id
	"""

	bot = get_bot(id)
	if not bot:
		return HTTPException(status_code=404, detail="Bot not found")

	if body.name:
		bot.name = body.name

	if body.prompt:
		bot.prompt = body.prompt

	if body.model_id:
		bot.model_id = body.model_id

	await save_bot(bot)

	return bot


@router.get("/default", response_model=Bot)
def get_default_bot():
	"""
	Returns the default bot
	"""

	return get_default_bot()


@router.patch("/default", response_model=Bot)
async def update_default_bot(body: UpdateBotRequest):
	"""
	Updates the default bot
	"""

	bot = get_default_bot()
	if not bot:
		return HTTPException(status_code=500, detail="Fatal: default bot not found")

	if body.name:
		bot.name = body.name

	if body.prompt:
		bot.prompt = body.prompt

	if body.model_id:
		bot.model_id = body.model_id

	await save_bot(bot)

	return bot