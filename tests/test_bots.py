from fastapi.testclient import TestClient
from app.main import app
from models.bot import Bot

from app.routers.bots.models import NewBotRequest, UpdateBotRequest

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
def bot_list():
	return []


def test_create_default_bot(bot_list):
	bot = NewBotRequest(
		name="default_bot",
		prompt="You are a bot that teaches about Islam",
		model_id="gpt-3.5-turbo-1106"
	)

	response = client.post("/bots", json=bot.dict(), headers=HEADERS)

	json = response.json()

	assert response.status_code == 200
	assert Bot(**json)

	bot = Bot(**json)
	assert bot.id != None
	bot_list.append(bot)


def test_get_default_bot(bot_list):
	response = client.get("/bots/default", headers=HEADERS)
	
	assert response.status_code == 200
	json = response.json()
	assert Bot(**json)
	assert json["name"] == "default_bot"


def test_create_bot(bot_list):
	bot = NewBotRequest(
		name="test_bot",
		prompt="You are a bot that teaches peopole about beautiful Islam",
		model_id=bot_list[0].model_id
	)
	response = client.post("/bots", json=bot.dict(), headers=HEADERS)

	json = response.json()
	
	assert response.status_code == 200
	assert Bot(**json)
	
	bot = Bot(**json)
	assert bot.id != None
	
	bot_list.append(bot)


def test_list_bots(bot_list):
	response = client.get("/bots", headers=HEADERS)
	assert response.status_code == 200
	json = response.json()

	assert isinstance(json, list)
	assert len(json) == len(bot_list)
	assert bot_list == [Bot(**bot_dict) for bot_dict in json]


def test_get_bot(bot_list):
	bot = bot_list[1]
	response = client.get(f"/bots/{bot.id}", headers=HEADERS)
	
	assert response.status_code == 200
	json = response.json()

	assert Bot(**json) == bot


def test_update_bot(bot_list):
	bot = bot_list[1]

	update = UpdateBotRequest(
		name="test_bot",
		prompt="You are a bot that teaches about Islam",
	)

	response = client.patch(f"/bots/{bot.id}", json=update.dict(), headers=HEADERS)

	assert response.status_code == 200
	json = response.json()

	assert bot.id == json["_id"]
	assert json["name"] == update.name
	assert json["prompt"] == update.prompt
	assert json["model_id"] == bot.model_id
	assert Bot(**json)

	bot_list[1] = Bot(**json)

	test_get_bot(bot_list)