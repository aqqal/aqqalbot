from fastapi import APIRouter, Depends, HTTPException
from app.auth import validate_token

from app.routers.chats.models import (
	NewChatRequest,
	NewMessageRequest
)

from bot.openai_assistants import create_new_chat, add_message, get_response
from models.chat import Chat, Message

from datastore.botstore_json import get_default_bot
from datastore.chatstore_json import get_chat, save_chat

from app import logger

router = APIRouter(
	prefix="/chats",
	tags=["chats"],
	dependencies=[Depends(validate_token)]
)


@router.post("/", response_model=Chat)
async def new_chat(body: NewChatRequest):
	"""
	Creates a new chat with the given bot_id
	"""
	bot_id = body.bot_id if body.bot_id else get_default_bot().id

	chat = await create_new_chat(bot_id)
	
	return save_chat(chat)



@router.get("/{chat_id}", response_model=Chat)
async def get_chat_from_datastore(chat_id: str):
	"""
	Returns a chat from datastore by id
	"""

	chat = get_chat(chat_id)
	if not chat:
		raise HTTPException(status_code=404, detail="Chat not found")

	return chat


@router.post("/{chat_id}/messages", response_model=Message)
async def new_message(chat_id: str, body: NewMessageRequest):
	"""
	Returns a response from the bot for the message added to the chat
	"""

	# get chat from datastore
	chat = get_chat(chat_id)
	if not chat:
		raise HTTPException(status_code=404, detail="Chat not found")

	if not body.content:
		raise HTTPException(status_code=400, detail="Message content required")

	message = await add_message(chat, body.content)
	response = await get_response(chat, message.content)

	return response