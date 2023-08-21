from pydantic import BaseModel
from typing import Optional, List
from models.Message import Message

class Chat(BaseModel):
	messages: List[Message]
