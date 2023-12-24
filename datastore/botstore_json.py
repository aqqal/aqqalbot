from models.bot import Bot
from typing import List, Union
import json
import os


JSON_FILE = os.path.dirname(os.path.realpath(__file__)) + "/bots.json"


def get_default_bot() -> Bot:
	"""
	Returns the default bot from datastore
	"""

	bots = []
	with open(JSON_FILE) as f:
		bots = json.load(f)

	bots = [Bot(**bot) for bot in bots]
	if len(bots) == 0:
		raise Exception("No bots found in datastore")

	return bots[0]


def get_bot(id: str) -> Union[Bot, None]:
	"""
	Returns a bot from datastore by id
	"""

	bots = []
	with open(JSON_FILE) as f:
		bots = json.load(f)

	bots = [Bot(**bot) for bot in bots]

	for bot in bots:
		if bot.id == id:
			return bot

	return None


async def save_bot(new_bot: Bot) -> Bot:
	"""
	Saves a bot to datastore, replacing a bot that already exists
	with the same id
	"""

	bots = []
	with open(JSON_FILE) as f:
		bots = json.load(f)

	# replace if exists
	for bot in bots:
		if bot["id"] == new_bot.id:
			bots.remove(bot)

	if new_bot.name == "default_bot":
		bots.insert(0, new_bot.dict())
	else:
		bots.append(new_bot.dict())

	with open(JSON_FILE, "w") as f:
		json.dump(bots, f, indent=2)

	return Bot(**new_bot.dict())


def list_bots() -> List[Bot]:
	"""
	Returns a list of all bots in datastore
	"""

	bots = []
	with open(JSON_FILE) as f:
		bots = json.load(f)

	bots = [Bot(**bot) for bot in bots]
	return bots
