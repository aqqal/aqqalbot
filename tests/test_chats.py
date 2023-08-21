from fastapi.testclient import TestClient
from app.main import app
from app.routes.chats.models import NewChatResponse, GetChatResponse, NewMessageResponse
from tests.logger import logger as test_logger
from dotenv import load_dotenv
import os
import pytest


load_dotenv()

token = os.getenv("CLIENT_KEY")
HEADERS = {
	'Authorization': f'Bearer {token}'
}

client = TestClient(app)

@pytest.fixture(scope="module")
def new_chat():
	response = client.post(
		"/chats",
		headers=HEADERS
	)
	test_logger.info("Received response for POST /chats: " + str(response.json()))
	yield {
		"new_chat_response": response,
		"chat_id": response.json()["chat_id"],
		"new_message": {
			"message_content": "Hello, I am aqqalbot",
		}
	}


@pytest.mark.order(1)
def test_new_chat(new_chat):
	response = new_chat["new_chat_response"]
	assert response.status_code == 200
	
	json = response.json()
	assert bool(NewChatResponse(**json)) == True


@pytest.mark.order(2)
def test_get_chat(new_chat):
	response = client.get(
		f"/chats/{new_chat['chat_id']}",
		headers=HEADERS
	)
	test_logger.info(f"Received response for GET /chats/{new_chat['chat_id']}: " + str(response.json()))

	assert response.status_code == 200
	
	json = response.json()
	assert bool(GetChatResponse(**json)) == True


@pytest.mark.order(3)
def test_add_message(new_chat):
	json = new_chat["new_message"]

	response = client.post(
		f"/chats/{new_chat['chat_id']}",
		json=json,
		headers=HEADERS
	)
	test_logger.info(f"Received response for POST /chats/{new_chat['chat_id']}: " + str(response.json()))

	assert response.status_code == 200
	
	json = response.json()
	assert bool(NewMessageResponse(**json)) == True


@pytest.mark.order(4)
def test_chats_config():
	pass
