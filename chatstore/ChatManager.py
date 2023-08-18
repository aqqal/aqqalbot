from chatstore.config import db as mongo_db
from models.Chat import Chat, Message
from ..logger import logger
from pymongo.objectid import ObjectId


class ChatManager():
	chats_collection = mongo_db["chats"]

	def __init__(self, chat_id: str = None, new_chat: Chat = None):
		if not chat_id:	
			if not new_chat:
				raise ValueError("Cannot instantiate ChatManager without existing chat id or new chat object")

			chat_id = self.chats_collection.insert_one(new_chat).inserted_id

		
		self.chat = self.chats_collection.find_one({ "_id": ObjectId(chat_id) })
		
		if not self.chat:
			raise ValueError("Could not find chat with id: " + chat_id)
		
		self.chat_id = ObjectId(chat_id)
		
	
	def add_message(self, new_message: Message):
		new_message = new_message.dict()
		self.chats_collection.find_one_and_update({ "_id": self.chat_id }, { "messages": { "$push": new_message } })

	@property
	def openai_conversation_json():
		pass

# /POST chat
# /GET/{id} chat
# /POST/{id} chat
