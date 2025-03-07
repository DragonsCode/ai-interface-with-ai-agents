from os import getenv
from apscheduler.schedulers.background import BackgroundScheduler


TG_BOT_TOKEN = getenv("TG_BOT_TOKEN")
OPENAI_API_KEY = getenv("OPENAI_API_KEY")
DB_USER = getenv("DB_USER", "root")
DB_PASSWORD = getenv("DB_PASSWORD", "password")
DB_HOST = getenv("DB_HOST", "localhost")
DB_PORT = getenv("DB_PORT", "3306")
DB_NAME = getenv("DB_NAME", "ai_interface")

scheduler = BackgroundScheduler()