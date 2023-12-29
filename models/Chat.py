from pydantic import BaseModel, Field
from typing import Optional, List, Union
from typing_extensions import Literal

from models.bot import Bot
from models.openai_context import OpenAIContext
import uuid

class TokenUsage(BaseModel):
	completion_tokens: Optional[int]
	prompt_tokens: Optional[int]
	tokens: int


class Message(BaseModel):
	created_at: int
	by: str
	content: str
	token_usage: Optional[TokenUsage]
	

class Chat(BaseModel):
	class Config:
		allow_population_by_field_name = True

	id: str = Field(default_factory=uuid.uuid4, alias="_id")
	bot: Bot
	created_at: int
	last_message: int
	messages: List[Message]
	model_context: Optional[OpenAIContext]

