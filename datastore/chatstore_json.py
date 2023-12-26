from models.chat import Chat
from typing import List, Union
import json
import os


JSON_FILE = os.path.dirname(os.path.realpath(__file__)) + "/chats.json"


def get_chat(id: str) -> Union[Chat, None]:
	"""
	Returns a chat from datastore by id
	"""

	chats = []
	with open(JSON_FILE) as f:
		chats = json.load(f)

	chats = [Chat(**chat) for chat in chats]

	for chat in chats:
		if chat.id == id:
			return chat

	return None


def save_chat(new_chat: Chat) -> Chat:
	"""
	Saves a chat to datastore, replacing a chat that already exists
	with the same id
	"""

	chats = []
	with open(JSON_FILE) as f:
		chats = json.load(f)

	# replace if exists
	for chat in chats:
		if chat["id"] == new_chat.id:
			chats.remove(chat)

	chats.append(new_chat.dict())

	with open(JSON_FILE, "w") as f:
		json.dump(chats, f, indent=2)

	return Chat(**new_chat.dict())


def list_chats() -> List[Chat]:
	"""
	Returns a list of all chats in datastore
	"""

	chats = []
	with open(JSON_FILE) as f:
		chats = json.load(f)

	chats = [Chat(**chat) for chat in chats]
	return chats