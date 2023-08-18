from pydantic import BaseModel
from typing import Optional, List


class Chat(BaseModel):
	messages: List[Message]
