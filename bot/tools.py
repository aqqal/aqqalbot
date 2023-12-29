from typing import List, Any
from models.chat import Chat

def get_available_tools():
	return None

def call_tools_on_chat(chat: Chat, tool_calls: List[Any]) -> Chat:
	return chat