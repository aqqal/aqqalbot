from pydantic import BaseModel
from typing import Optional

class Bot(BaseModel):
	id: Optional[str]
	name: str
	created_at: int
	prompt: str
	model_id: str
