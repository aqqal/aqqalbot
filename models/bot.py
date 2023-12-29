from pydantic import BaseModel, Field
import uuid


class Bot(BaseModel):
	class Config:
		allow_population_by_field_name = True
		
	id: str = Field(default_factory=uuid.uuid4, alias="_id")
	name: str
	created_at: int
	prompt: str
	model_id: str