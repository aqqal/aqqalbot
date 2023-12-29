from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from app.auth import validate_token
from typing import List
from uuid import uuid4
import time

from app.routers.bots.models import (
	NewBotRequest,
	UpdateBotRequest,
)

from datastore.mongoconfig import chat_db

from models.bot import Bot
from app.logger import logger

router = APIRouter(
    prefix="/bots",
    dependencies=[Depends(validate_token)]
)

@router.post("", response_model=Bot)
async def new_bot(body: NewBotRequest):
	"""
	Creates a new bot
	"""
	# check if bot with name already exists in mongo
	bot = chat_db.bots.find_one({"name": body.name})
	if bot:
		raise HTTPException(status_code=400, detail="Bot with name already exists")


	bot = Bot(
		name=body.name,
		prompt=body.prompt,
		model_id=body.model_id,
		created_at=int(time.time())
	)

	bson = jsonable_encoder(bot, by_alias=True)
	inserted_id = chat_db.bots.insert_one(bson).inserted_id

	if bson["_id"] != inserted_id:
		raise HTTPException(status_code=500, detail="Errosr saving bot to db")

	logger.info(f"Saved new bot: {bot}")
	return jsonable_encoder(bot, by_alias=False)


@router.get("", response_model=List[Bot])
async def get_bots():
	"""
	Returns a list of all bots
	"""

	# get all bots from mongo
	bots = chat_db.bots.find()
	models = [Bot(**bot) for bot in bots]	

	return jsonable_encoder(models, by_alias=False)	



@router.get("/default", response_model=Bot)
async def default_bot():
	"""
	Returns the default bot
	"""

	# get default bot from mongo
	bot = chat_db.bots.find_one({"name": "default_bot"})
	if not bot:
		raise HTTPException(status_code=500, detail="Fatal: default bot not found")
	
	return jsonable_encoder(Bot(**bot).dict(), by_alias=False)


@router.patch("/default", response_model=Bot)
async def update_default_bot(body: UpdateBotRequest):
	"""
	Updates the default bot. Does not allow changing the name of default bot.
	"""

	bot = chat_db.bots.find_one({"name": "default_bot"})
	if not bot:
		raise HTTPException(status_code=500, detail="Fatal: default bot not found")

	body = body.dict()
	update = body.copy()
	
	for key in body:
		if body[key] == None:
			update.pop(key)
			continue

		if key == "name":
			raise HTTPException(status_code=400, detail="Cannot change name of default bot")
		
	chat_db.bots.update_one({"name": "default_bot"}, {"$set": update})
	return default_bot()


@router.get("/{id}", response_model=Bot)
async def get_bot_by_id(id: str):
	"""
	Gets a bot by id
	"""
	
	bot = chat_db.bots.find_one({"_id": id})
	if not bot:
		raise HTTPException(status_code=404, detail="Bot not found")

	return jsonable_encoder(bot, by_alias=False)


@router.patch("/{id}", response_model=Bot)
async def update_bot_by_id(id: str, body: UpdateBotRequest):
	"""
	Updates a bot by id. Does not allow changing the name of default bot.
	"""

	bot = chat_db.bots.find_one({"_id": id})

	if not bot:
		raise HTTPException(status_code=404, detail="Bot not found")

	body = body.dict()

	update = body.copy()
	for key in body:
		if body[key] == None:
			update.pop(key)
			continue

		if key == "name" and bot["name"] == "default_bot":
			raise HTTPException(status_code=400, detail="Cannot change name of default bot")
		
		
	chat_db.bots.update_one({"_id": id}, {"$set": update})

	bot = chat_db.bots.find_one({"_id": id})
	return jsonable_encoder(bot, by_alias=True)