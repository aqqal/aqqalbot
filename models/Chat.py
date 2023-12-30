from pydantic import BaseModel, Field
from typing import Optional, List, Union
from typing_extensions import Literal

from models.bot import Bot
from models.openai_context import OpenAIContext
import uuid

import time

class TokenUsage(BaseModel):
	completion_tokens: Optional[int]
	prompt_tokens: Optional[int]
	tokens: int


class Message(BaseModel):
	created_at: int = Field(default_factory=lambda:int(time.time()))
	by: Literal["user", "bot"]
	content: str
	

class Chat(BaseModel):
	class Config:
		allow_population_by_field_name = True

	id: str = Field(default_factory=uuid.uuid4, alias="_id")
	bot: Bot
	created_at: int = Field(default_factory=lambda:int(time.time()))
	last_message: int = 0
	messages: List[Message] = []
	model_context: Optional[OpenAIContext] = None