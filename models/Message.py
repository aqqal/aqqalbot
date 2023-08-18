from pydantic import BaseModel
from typing import Optional, List


class Message(BaseModel):
	bot: bool # True if message is sent by bot
	timestamp: int
	text: str
	user_id: Optional[str]