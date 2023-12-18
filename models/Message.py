from pydantic import BaseModel
from typing import Optional, List


class TokenUsage(BaseModel):
	completion_tokens: int
	prompt_tokens: int
	total_tokens: int


class Message(BaseModel):
	id: str
	bot: bool
	content: str
	context: Optional[str]
	token_usage: Optional[TokenUsage] # dict of token usage for the response