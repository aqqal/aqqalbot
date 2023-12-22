from pydantic import BaseModel
from typing import Optional, List
from models.Message import Message

class Chat(BaseModel):
	id: Optional[str]
	created_at: int
	last_message: int
	bot_id: str
	messages: Optional[List[Message]]


class Message(BaseModel):
	id: Optional[str]
	created_at: int
	by: str
	content: str
	context: Optional[str]
	token_usage: Optional[TokenUsage]


class TokenUsage(BaseModel):
	completion_tokens: Optional[int]
	prompt_tokens: Optional[int]
	tokens: int