from fastapi.testclient import TestClient
from app.main import app
from models.chat import Chat, Message

from app.routers.chats.models import NewChatRequest, NewMessageRequest

from tests.logger import logger as test_logger
from dotenv import load_dotenv
import os
import pytest

load_dotenv()

client = TestClient(app)

token = os.getenv("CLIENT_KEY")

HEADERS = {
	'Authorization': f'Bearer {token}'
}


@pytest.fixture(scope="module")
def chat_info():
	return {
		"test_bot_name": "test_bot",
	}


def test_new_chat_default_bot(chat_info):
	"""
	Tests the endpoint POST /chats with empty body
	"""

	body = NewChatRequest()

	response = client.post(
		"/chats",
		json=body.dict(),
		headers=HEADERS
	)

	assert response.status_code == 200
	json = response.json()
	assert Chat(**json)
	chat = Chat(**json)
	assert chat.id is not None
	assert chat.last_message == 0
	assert chat.bot.name == "default_bot"
	
	chat_info["chat_id"] = chat.id


def test_get_chat(chat_info):
	"""
	Tests the endpoint GET /chats/{chat_id}
	"""

	response = client.get(
		f"/chats/{chat_info['chat_id']}",
		headers=HEADERS
	)

	assert response.status_code == 200
	json = response.json()
	assert Chat(**json)
	chat = Chat(**json)

	assert chat.id == chat_info["chat_id"]

	

def test_new_chat_custom_bot(chat_info):
	"""
	Tests the endpoint POST /chats with bot_id specified
	"""

	body = NewChatRequest(
		bot_name=chat_info["test_bot_name"]
	)

	response = client.post(
		"/chats",
		json=body.dict(),
		headers=HEADERS
	)

	assert response.status_code == 200
	json = response.json()
	assert Chat(**json)
	chat = Chat(**json)
	assert chat.id is not None
	assert chat.last_message == 0
	assert chat.bot.name == chat_info["test_bot_name"]
	
	chat_info["chat_id"] = chat.id


def test_new_message(chat_info):
	"""
	Tests the endpoint POST /chats/{chat_id}/messages
	"""

	body = NewMessageRequest(
		content="Are you gonna pass this test?",
	)

	response = client.post(
		f"/chats/{chat_info['chat_id']}/messages",
		json=body.dict(),
		headers=HEADERS
	)

	assert response.status_code == 200
	json = response.json()
	assert Message(**json)
	message = Message(**json)
	assert message.by == "bot"