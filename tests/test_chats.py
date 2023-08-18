from fastapi.testclient import TestClient
from app.main import app
from app.routes.chats.models import NewChatResponse, GetChatResponse, NewMessageResponse

from dotenv import load_dotenv
import os
import pytest


load_dotenv()

token = os.getenv("CLIENT-TOKEN")
HEADERS = {
	'Authorization': f'Bearer {token}'
}

client = TestClient(app)

@pytet.fixture(scope="module")
def new_chat():
	response = client.post(
		"/chats",
		headers=HEADERS
	)
	yield {
		"new_chat_response": response,
		"chat_id": response.json()["chat_id"],
		"new_message": {
			"bot": True,
			"timestamp": 123456789,
			"text": "Hello, I am aqqalbot",
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

	assert response.status_code == 200
	
	json = response.json()
	assert bool(GetChatResponse(**json)) == True


@pytest.mark.order(3)
def test_add_message(new_chat):
	json = {
		"message": new_chat["new_message"]
	}

	response = client.post(
		f"/chats/{new_chat['chat_id']}",
		json=json,
		headers=HEADERS
	)

	assert response.status_code == 200
	
	json = response.json()
	assert bool(NewMessageResponse(**json)) == True


@pytest.mark.order(4)
def test_chats_config():
	pass
