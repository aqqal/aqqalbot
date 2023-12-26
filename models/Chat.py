from pydantic import BaseModel
from typing import Optional, List


class TokenUsage(BaseModel):
	completion_tokens: Optional[int]
	prompt_tokens: Optional[int]
	tokens: int


class Message(BaseModel):
	id: Optional[str]
	chat_id: str
	created_at: int
	by: str
	content: str
	context: Optional[str]
	token_usage: Optional[TokenUsage]
	

class Chat(BaseModel):
	id: Optional[str]
	created_at: int
	last_message: int
	bot_id: str

