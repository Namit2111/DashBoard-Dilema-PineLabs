from dotenv import load_dotenv
import os
load_dotenv()

DB_PATH = os.getenv("DB_PATH")
OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

