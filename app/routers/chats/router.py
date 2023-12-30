from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from app.auth import validate_token

from app.routers.chats.models import (
	NewChatRequest,
	NewMessageRequest
)

from models.chat import Chat, Message
from models.bot import Bot

from datastore.mongoconfig import chat_db

from bot.openai_completions import (
	add_init_model_context_to_chat,
	add_bot_response_to_chat,
	add_user_message_to_chat
)

from app.logger import logger
import time

chats_collection = chat_db.get_collection("chats")
bots_collection = chat_db.get_collection("bots")

router = APIRouter(
	prefix="/chats",
	tags=["chats"],
	dependencies=[Depends(validate_token)]
)


@router.post("/")
async def new_chat(body: NewChatRequest):
	"""
	Creates a new chat with the given bot_id
	"""
	bot = None
	if not body.bot_id and not body.bot_name:
		bot = bots_collection.find_one({"name": "default_bot"})
		if not bot:
			logger.error("Fatal: default bot not found")
			raise HTTPException(status_code=500, detail="Fatal: default bot not found")


	# try retrieving by id, then by name
	bot = bots_collection.find_one({"_id": body.bot_id}) if (not bot) and body.bot_id else bot
	bot = bots_collection.find_one({"name": body.bot_name}) if (not bot) and body.bot_name else bot

	if not bot:
		raise HTTPException(status_code=400, detail="Bot not found")

	
	chat = Chat(
		bot=bot,
	)

	chat = await add_init_model_context_to_chat(chat)
	chat = jsonable_encoder(chat)

	inserted_id = chats_collection.insert_one(chat).inserted_id
	if inserted_id != chat["_id"]:
		raise HTTPException(status_code=500, detail="Error creating chat")

	# validate before excluding context
	chat = Chat(**chat)
	logger.info(f"New chat created with id {inserted_id}")

	res = jsonable_encoder(chat, exclude=["model_context"])
	return res



@router.get("/{chat_id}", response_model=Chat)
async def get_chat_from_datastore(chat_id: str):
	"""
	Returns a chat from datastore by id
	"""

	chat = chats_collection.find_one({"_id": chat_id})
	if not chat:
		raise HTTPException(status_code=404, detail="Chat not found")

	chat = Chat(**chat)
	res = jsonable_encoder(chat, exclude=["model_context"])
	return res


@router.post("/{chat_id}/messages")
async def new_message(chat_id: str, body: NewMessageRequest):
	"""
	Returns a response from the bot for the message added to the chat
	"""

	# get chat from datastore
	chat = chats_collection.find_one({"_id": chat_id})

	if not chat:
		raise HTTPException(status_code=404, detail="Chat not found")

	if not body.content:
		raise HTTPException(status_code=400, detail="Message content required")

	chat = Chat(**chat)
	chat = await add_user_message_to_chat(chat, body.content)
	chat, message = await add_bot_response_to_chat(chat)

	chats_collection.find_one_and_update({"_id": chat_id}, {"$set": jsonable_encoder(chat)})
	chat = chats_collection.find_one({"_id": chat_id})

	if not chat:
		raise HTTPException(status_code=500, detail="Could not update chat")
	
	logger.info(f"New message added to chat {chat_id}")

	return jsonable_encoder(message)