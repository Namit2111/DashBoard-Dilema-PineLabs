from dotenv import load_dotenv
import os
load_dotenv()

DB_PATH = os.getenv("DB_PATH")
OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")


