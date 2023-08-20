import openai
from models.Message import Message
from typing import Tuple
import time
from bot.config import initial_params, openai_api_key


def generate_bot_message(messages: list, system: bool = False, **custom_params) -> Tuple[Message, dict]:
	"""
	Generates a response to a list of messages using the OpenAI API.
	Returns a 2 item tuple with a Message object and a dict of the token usage for the response.

	messages: list of message dicts with keys 'role' and 'content'

	"""

	# the params that will be sent to the openai api
	completion_params = initial_params.copy()
	completion_params.pop('system_message')

	valid_params = list(initial_params.keys())
	for param in custom_params:
		if param not in valid_params:
			raise ValueError(f"Invalid keyword argument: {param}")

		completion_params[param] = custom_params[param]

	response = get_openai_response(messages, **completion_params)
	message_object = response.choices[0]['message']
	role, content = message_object['role'], message_object['content']

	token_usage = response["usage"]

	return Message(timestamp=int(time.time()), role=role, content=content, token_usage=token_usage)


def get_openai_response(messages, **completion_params):
	try:
		logger.info("Sending OpenAI API completion request")
		response = openai.ChatCompletion.create(api_key=openai_api_key, messages=messages, **completion_params)
		logger.info("Received OpenAI API completion response")
	except Exception as e:
		logger.error("Error while sending OpenAI API completion request: " + str(e))
		raise e

	return response


def generate_system_message(message: str = None):
	if not message:
		message = initial_params['system_message']

	return Message(timestamp=int(time.time()), role="system", content=message)