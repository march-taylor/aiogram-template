import os
from dotenv import load_dotenv


load_dotenv()

class Config:
	BOT_TOKEN = os.getenv("BOT_TOKEN")
	DEFAULT_LANGUAGE = "en"
	DB_URL = "sqlite+aiosqlite:///bot.db"