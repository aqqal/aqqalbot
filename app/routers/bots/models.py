from pydantic import BaseModel
from typing import Optional
from models.Chat import Bot

class NewBotRequest(BaseModel):
	name: Optional[str]
	prompt: str
	model_id: str

class UpdateBotRequest(BaseModel):
	name: Optional[str]
	prompt: Optional[str]
	model_id: Optional[str]

