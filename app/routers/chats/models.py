from pydantic import BaseModel
from typing import Optional

class NewChatRequest(BaseModel):
	bot_id: Optional[str]
	bot_name: Optional[str]

class NewMessageRequest(BaseModel):
	content: str