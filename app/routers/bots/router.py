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

from bot.openai import create_new_bot, update_bot
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


@router.get("/default", response_model=Bot)
async def default_bot():
	"""
	Returns the default bot
	"""

	bot = get_default_bot()
	if not bot:
		return HTTPException(status_code=500, detail="Fatal: default bot not found")
	
	return bot


@router.patch("/default", response_model=Bot)
async def update_default_bot(body: UpdateBotRequest):
	"""
	Updates the default bot. Does not allow changing the name of default bot.
	"""

	bot = get_default_bot()
	if not bot:
		return HTTPException(status_code=500, detail="Fatal: default bot not found")

	body = body.dict()

	update = body.copy()
	for key in body:
		if body[key] == None:
			update.pop(key)
			continue

		if key == "name":
			return HTTPException(status_code=400, detail="Cannot change name of default bot")
		
		setattr(bot, key, update[key])

	await update_bot(bot.id, **update)
	bot = await save_bot(bot)

	return bot


@router.get("/{id}", response_model=Bot)
async def get_bot_by_id(id: str):
	"""
	Gets a bot by id
	"""

	bot = get_bot(id)
	if not bot:
		return HTTPException(status_code=404, detail="Bot not found")

	return bot


@router.patch("/{id}", response_model=Bot)
async def update_bot_by_id(id: str, body: UpdateBotRequest):
	"""
	Updates a bot by id. Does not allow changing the name of default bot.
	"""

	bot = get_bot(id)

	if not bot:
		return HTTPException(status_code=404, detail="Bot not found")

	body = body.dict()

	update = body.copy()
	for key in body:
		if body[key] == None:
			update.pop(key)
			continue

		if key == "name" and bot.name == "default_bot":
			return HTTPException(status_code=400, detail="Cannot change name of default bot")
		
		setattr(bot, key, body[key])

	await update_bot(bot.id, **update)
	bot = await save_bot(bot)

	return bot