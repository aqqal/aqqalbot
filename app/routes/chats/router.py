from fastapi import APIRouter, Depends
from bot.bot import generate_bot_message
from app.auth import validate_token
from chatstore.ChatManager import ChatManager

from models.Message import Message
from app.routes.chats.models import (
	NewChatResponse,
	NewMessageRequest,
	NewMessageResponse
)

import time

router = APIRouter(
	prefix="/chats",
    dependencies=[Depends(validate_token)]
)

@router.post("", response_model=NewChatResponse)
def new_chat():
	new_chat = ChatManager()
	
	return {
		"chat_id": str(new_chat.chat_id)
	}

@router.get("/{id}")
def get_chat(id: str):
	chat_manager = ChatManager(chat_id=id)
	chat = chat_manager.chat
	chat.pop("_id")
	chat_copy = chat.copy()

	return {
		"chat_id": id,
		"chat": chat
	}

@router.post("/{id}", response_model=NewMessageResponse)
def add_message(id: str, body: NewMessageRequest):
	# save message to chat and db
	chat_manager = ChatManager(chat_id=id)
	new_message = Message(
		role="user",
		content=body.message_content,
		timestamp=time.time()
	)

	chat_manager.add_message(new_message)

	all_messages = chat_manager.get_messages(for_completion=True)

	# generate bot response
	bot_response = generate_bot_message(messages=all_messages)

	# save bot response
	chat_manager.add_message(bot_response)
	chat = chat_manager.chat
	chat.pop("_id")
	chat_copy = chat.copy()

	return {
		"response": bot_response.content,
		"chat_id": id,
		"chat": chat_copy
	}

# --------Not implemented yet----------------

# @router.delete("/chats/{id}")
# def delete_chat(id: str):
# 	pass

# @router.delete("/chats")
# def delete_chats():
# 	pass

# @router.patch("/chats/config", response_model=ChatConfigResponse)
# def config_chat(body=ChatConfigRequest):
# 	pass