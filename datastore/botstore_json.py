def get_default_bot() -> Bot:
	"""
	Returns the default bot from datastore
	"""

	with open("bots.json") as f:
		bots = json.load(f)

	bots = [Bot(**bot) for bot in bots]
	if len(bots) == 0:
		raise Exception("No bots found in datastore")

	return bots[0]


def get_bot(id: str) -> Bot | None:
	"""
	Returns a bot from datastore by id
	"""

	with open("bots.json") as f:
		bots = json.load(f)

	bots = [Bot(**bot) for bot in bots]
	
	for bot in bots:
		if bot.id == id:
			return bot

	return None

async def save_bot(new_bot: Bot):
	"""
	Saves a bot to datastore, replacing a bot that already exists
	with the same name or id
	"""

	bots = []
	with open("bots.json") as f:
		bots = json.load(f)

	# replace if exists
	for bot in bots:
		if bot["id"] == bot.id or bot["name"] == bot.name:
			bots.remove(bot)

			assitant_id = bot.pop("id")
			await client.beta.assistants.update(assistant_id, **bot.dict())

	if new_bot.name == "default_bot":
		bots.insert(0, new_bot.dict())
	else:
		bots.append(new_bot.dict())

	with open("bots.json", "w") as f:
		json.dump(bots, f)

	return new_bot

def list_bots() -> List[Bot]:
	"""
	Returns a list of all bots in datastore
	"""

	with open("bots.json") as f:
		bots = json.load(f)

	bots = [Bot(**bot) for bot in bots]
	return bots
