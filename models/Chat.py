from pydantic import BaseModel
from typing import Optional, List, Union
from typing_extensions import Literal

from models.bot import Bot
from models.openai import OpenAIContext


class TokenUsage(BaseModel):
	completion_tokens: Optional[int]
	prompt_tokens: Optional[int]
	tokens: int


class Message(BaseModel):
	created_at: int
	by: str
	content: str
	token_usage: Optional[TokenUsage] = None
	

class Chat(BaseModel):
	id: Optional[str]
	bot: Bot
	created_at: int
	last_message: int
	messages: List[Message]
	model_context: Optional[OpenAIContext] = []

