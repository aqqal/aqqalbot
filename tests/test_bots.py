from fastapi.testclient import TestClient
from app.main import app
from models.bot import Bot

from app.routers.bots.models import NewBotRequest, UpdateBotRequest

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

# Test Bot

@pytest.fixture(scope="module")
def bot_list():
	return []	


def test_get_default_bot(bot_list):
	response = client.get("/bots/default", headers=HEADERS)
	
	assert response.status_code == 200
	json = response.json()
	assert Bot(**json)

	bot_list.append(Bot(**json))
	assert json["name"] == "default_bot"


def test_create_bot(bot_list):
	bot = NewBotRequest(
		name="Test Bot",
		prompt="You are a bot that teaches about Islam",
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

