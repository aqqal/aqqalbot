from pymongo import MongoClient
from dotenv import load_dotenv
from app.logger import logger
import os

load_dotenv()

config = {
	'ENV': os.getenv('ENV'),
	'MONGO_HOST': os.getenv('MONGO_HOST'),
	'MONGO_PORT': os.getenv('MONGO_PORT'),
	'ATLAS_CONNECTION_STR': os.getenv('ATLAS_CONNECTION_STR'),
	'MONGO_DB': os.getenv('MONGO_DB')
}

def get_db():
	"""Return Mongo database connection."""
	
	try:
		if config['ENV'] == 'PROD':
			logger.info("Connecting to mongo")
			client = MongoClient(config['MONGO_HOST'], int(config['MONGO_PORT']))
		else:
			# use atlas for dev
			logger.info("Connecting to atlas")
			client = MongoClient(config['ATLAS_CONNECTION_STR'])

		db = client[config['MONGO_DB']]
	except Exception as e:
		logger.error('Error connecting to database: {}'.format(e))
		raise e
	else:
		return db, client

db, client = get_db()