from chatstore.config import db as mongo_db
from models.Chat import Chat, Message
from bot.bot import generate_system_message
from app.logger import logger
from bson.objectid import ObjectId


class ChatManager():
	chats_collection = mongo_db["chats"]

	def __init__(self, chat_id: str = None):
		if not chat_id:
			
			# create a new chat on empty instance creation
			try:
				new_chat = self.__create_chat__()	
				chat_id = self.chats_collection.insert_one(new_chat).inserted_id
				logger.info("Created new chat with id: " + str(chat_id))
			except Exception as e:
				logger.error("Error while creating new chat: " + str(e))
				raise e
				
		if not self.chat:
			raise ValueError("Could not find chat with id: " + chat_id)
		
		self.chat_id = ObjectId(chat_id)


	@property
	def chat(self) -> dict:
		"""
		The chat document in mongodb.
		Note: A database query for the chat with the given id is called on eachproperty access.
		
		"""

		chat = self.chats_collection.find_one({ "_id": ObjectId(self.chat_id) })
		return chat


	def __create_chat__(self) -> dict:
		system_message = generate_system_message()
		new_chat = Chat(messages=[system_message])
		return new_chat.dict()
		
	
	def add_message(self, new_message: Message):
		self.chats_collection.find_one_and_update({ "_id": self.chat_id }, { "messages": { "$push": new_message.dict() } })


	def get_messages(self, for_completion = False, last_n: int = None):
		try:
			messages = self.chat["messages"]
			logger.info("DB Read messages from chat with id: " + self.chat_id)
		except Exception as e:
			logger.error("Error while reading messages from chat with id: " + self.chat_id + " : " + str(e))
			raise e
		
		if last_n:
			messages = messages[len(messages) - last_n:]

		if for_completion:
			messages_list = []
			for message in messages:
				messages_list.append({
					'role' : message['role'],
					'content': message['content']
				})

			return messages_list

		return messages




# /POST chat
# /GET/{id} chat
# /POST/{id} chat
