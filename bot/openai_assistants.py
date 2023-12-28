from models.chat import Chat, Message
from models.bot import Bot

from bot.config import client
from bot.logger import logger
import time

async def create_new_bot(model_id: str, prompt: str, name=None) -> Bot:
	"""
	Creates a new OpenAI assistant from the given model and instructions
	Returns a Bot object

	"""	

	assistant = await client.beta.assistants.create(
		model=model_id,
		instructions=prompt,
		name=name
	)

	return Bot(id=assistant.id, name=assistant.name, created_at=assistant.created_at, prompt=prompt, model_id=model_id)


async def update_bot(id, *args, **kwargs) -> Bot:
	"""
	Updates an OpenAI assistant with the given bot object
	Returns the updated Bot object
	"""

	if "prompt" in kwargs:
		kwargs["instructions"] = kwargs["prompt"]
		del kwargs["prompt"]
	
	if "model_id" in kwargs:
		kwargs["model"] = kwargs["model_id"]
		del kwargs["model_id"]

	assistant = await client.beta.assistants.update(id, **kwargs)
	return Bot(id=assistant.id, name=assistant.name, created_at=assistant.created_at, prompt=assistant.instructions, model_id=assistant.model)


async def create_new_chat(bot_id: str) -> Chat:
	"""
	Returns a new Chat object by creating a new OpenAI thread
	"""

	thread = await client.beta.threads.create()
	return Chat(id=thread.id, created_at=thread.created_at, last_message=thread.created_at, bot_id=bot_id)


async def poll_run(run_id: str, chat: Chat) -> str:
	"""
	Polls the OpenAI API for the status of a run on a Thread
	Returns the status
	"""

	run = await client.beta.threads.runs.retrieve(run_id, thread_id=chat.id)
	return run.status


async def create_run(chat: Chat) -> str:
	"""
	Creates a new run on an OpenAI thread
	Returns the run id
	"""

	run = await client.beta.threads.runs.create(thread_id=chat.id, assistant_id=chat.bot_id)
	return run.id


async def add_message(chat: Chat, content: str, context: str = None) -> Message:
	"""
	Adds a message to an OpenAI thread
	Returns the response from OpenAI
	"""

	message = await client.beta.threads.messages.create(chat.id, role="user", content=content)
	
	return Message(
		id=message.id,
		created_at=message.created_at,
		by="user",
		content=content,
		chat_id=chat.id
	)


async def get_response(chat: Chat, message: str, context: str = None, timeout_seconds=60) -> Message:
	"""
	Gets the response from an OpenAI thread
	Returns the response from OpenAI
	"""
	valid_statuses = ["queued", "in_progress", "completed"]

	run_id = await create_run(chat)
	status = await poll_run(run_id, chat)

	c = timeout_seconds
	
	while True:
		if status == "completed":
			break

		time.sleep(1)
		c -= 1
		if c == 0:
			raise TimeoutError("Timeout while waiting for Run to complete")

		if status not in valid_statuses:
			raise Exception("Unexpected Run status returned from OpenAI: " + status)

		status = await poll_run(run_id, chat)
	
	if status != "completed":
		raise Exception("Unexpected Run status returned from OpenAI: " + status)

	# get the last run step
	message_creation_run_step = await client.beta.threads.runs.steps.list(run_id, thread_id=chat.id)
	message_creation_run_step = message_creation_run_step.data[-1]


	if message_creation_run_step.step_details.type != "message_creation":
		raise Exception("Expected message creation step, received this step type returned from OpenAI: " +
		                message_creation_run_step.step_details.type)

	if message_creation_run_step.status != "completed":
		raise Exception("Expected complete message creation, received this run step status returned from OpenAI: " + message_creation_run_step.status)
	
	message_id = message_creation_run_step.step_details.message_creation.message_id
	message = await client.beta.threads.messages.retrieve(message_id, thread_id=chat.id)
	content = message.content[0].text.value

	return Message(
		id=message.id,
		created_at=message.created_at,
		by="bot",
		content=content,
		chat_id=chat.id
	)