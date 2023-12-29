import pymongo
from dotenv import load_dotenv
import os
from .logger import logger

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
CHAT_DB_NAME = "chatDB"

def get_client():
	try:
		client = pymongo.MongoClient(MONGO_URL)
	except Exception as e:
		logger.error("Error connecting to MongoDB")
		raise e		
	return client

client = get_client()
chat_db = client.get_database(CHAT_DB_NAME)