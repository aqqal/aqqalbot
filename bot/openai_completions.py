
from models.chat import Chat, Message
from models.bot import Bot
from models.openai_context import OpenAIContext

from bot.config import client
from bot.tools import get_available_tools, call_tools_on_chat
from bot.logger import logger

import time

async def add_init_model_context_to_chat(chat: Chat) -> Chat:
	"""
	Adds initial model context array item to chat object by reading bot object in the chat.
	
	"""

	if chat.model_context:
		raise Exception("Model context already exists")

	context = {
		'messages': [
			{
				'role': 'system',
				'content': chat.bot.prompt
			}
		]
	}

	chat.model_context = OpenAIContext(**context)
	return chat
	

async def add_user_message_to_chat(chat: Chat, content: str) -> Chat:
	"""
	Appends a user Message to chat object.
	"""

	message = Message(
		content=content,
		by="user",
	)

	chat.last_message = message.created_at

	if not chat.model_context:
		raise Exception("Chat object not initialized")

	chat.messages.append(message)
	chat.model_context.messages.append({
		"role": "user",
		"content": content,
	})

	return chat

async def add_bot_response_to_chat(chat: Chat, use_tools=False) -> Chat:
	"""
	Uses bot in chat object to append a response Message using OpenAI.
	"""

	logger.info(f"Calling OpenAI")
	openai_response = await client.chat.completions.create(
		messages=chat.model_context.messages,
		model=chat.bot.model_id,
	)
	logger.info(f"Received OpenAI response: {openai_response}")
	
	openai_message = openai_response.choices[0].message
	chat.model_context.messages.append(openai_message)
	
	content = openai_message.content
	tool_calls = openai_message.tool_calls
	
	if not use_tools or not tool_calls:
		if not content:
			raise Exception("No content returned from OpenAI")

		timestamp = int(time.time())
		message = Message(
			content=content,
			by="bot",
			created_at=timestamp,
		)

		chat.last_message = timestamp
		chat.messages.append(message)

		return chat, message


	chat = await call_tools_on_chat(chat, tool_calls)
	return add_bot_response_to_Chat(chat, use_tools=use_tools)