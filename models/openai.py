from typing import List, Optional, Literal
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall


class OpenAIMessage(BaseModel):
	role: Literal["system", "assitant", "tool", "user"]
	"""The role of the author of this message."""
	
	content: Optional[str]
	"""The contents of the message."""

	tool_calls: Optional[List[ChatCompletionMessageToolCall]] = None
	"""The tool calls generated by the model, such as function calls."""


class OpenAIContext(BaseModel):
	messages = List[OpenAIMessage]