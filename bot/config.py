from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

# initial param values for openai response generation

initial_params = {}

with open("params.json", "r") as f:
	initial_params = json.load(f)