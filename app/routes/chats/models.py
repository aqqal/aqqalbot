from pydantic import BaseModel
from typing import List, Optional
from aqqalbot.models import Chat, Message


class NewChatRequest(BaseModel):
	chat: Chat


class NewChatResponse(BaseModel):
	chat_id: str


class GetChatResponse(BaseModel):
	chat_id: str
	chat: Chat


class NewMessageRequest(BaseModel):
	message: Message


class NewMessageResponse(BaseModel):
	response: str
	chat: Chat


class ChatConfigResponse(BaseModel):
	pass


class ChatConfigRequest(BaseModel):
	pass