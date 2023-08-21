from dotenv import load_dotenv
import os
import json

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

# initial param values for openai response generation

initial_params = {}

dir_path = os.path.dirname(os.path.abspath(__file__))

with open(dir_path + '//params.json', "r") as f:
	initial_params = json.load(f)