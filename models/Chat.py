from pydantic import BaseModel
from typing import Optional, List
from models.Message import Message


class Chat(BaseModel):
	id: str
	started_timestamp: int
	last_message_timestamp: int
	bot_version_id: str
	messages: List[Message]


class BotVersion(BaseModel):
	id: str
	name: str
	timestamp: int
	prompt: str