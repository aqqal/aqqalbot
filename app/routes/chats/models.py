from pydantic import BaseModel
from typing import List, Optional
from models.Chat import Chat
from models.Message import Message


class NewChatResponse(BaseModel):
	chat_id: str


class GetChatResponse(BaseModel):
	chat_id: str
	chat: Chat


class NewMessageRequest(BaseModel):
	message: Message


class NewMessageResponse(BaseModel):
	response: str
	chat_id: str
	chat: Chat


class ChatConfigResponse(BaseModel):
	pass


class ChatConfigRequest(BaseModel):
	pass