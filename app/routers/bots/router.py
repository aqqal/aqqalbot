from fastapi import APIRouter, Depends, HTTPException
from app.auth import validate_token
from typing import List

from app.routers.bots.models import (
	NewBotRequest,
	UpdateBotRequest,
)

from datastore.botstore_json import (
	get_default_bot,
	list_bots,
	save_bot,
	get_bot
)

from bot.openai import create_new_bot
from models.bot import Bot
from app import logger

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
	
	bot = await create_new_bot(body.model_id, body.prompt, body.name)
	await save_bot(bot)

	return bot 


@router.get("", response_model=List[Bot])
async def get_bots():
	"""
	Returns a list of all bots
	"""

	return list_bots()


@router.get("/{id}", response_model=Bot)
async def get_bot(id: str):
	"""
	Gets a bot by id
	"""

	bot = get_bot(id)
	if not bot:
		return HTTPException(status_code=404, detail="Bot not found")


@router.patch("/{id}", response_model=Bot)
async def update_bot(id: str, body: UpdateBotRequest):
	"""
	Updates a bot by id
	"""

	bot = get_bot(id)

	if not bot:
		return HTTPException(status_code=404, detail="Bot not found")

	body = body.dict()

	for key in body:
		if body[key] != None:
			setattr(bot, key, body[key])

	await save_bot(bot)
	return bot


@router.get("/default", response_model=Bot)
def defualt_bot():
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

	body = body.dict()

	for key in body:
		if body[key] != None:
			setattr(bot, key, body[key])

	await save_bot(bot)
	return bot