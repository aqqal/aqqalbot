from pydantic import BaseModel
from typing import Optional, List
from models.Message import Message

class Chat(BaseModel):
	id: Optional[str]
	created_at: int
	last_message: int
	bot_id: str
	messages: Optional[List[Message]]


class Bot(BaseModel):
	id: Optional[str]
	name: str
	created_at: int
	prompt: str
	model_id: str