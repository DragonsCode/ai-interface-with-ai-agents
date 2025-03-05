import asyncio
import logging
from os import getenv
from swarm import Swarm
from aiogram import Bot, Dispatcher

from handlers.voice import voice_router
from handlers.commands import commands_router
from handlers.basic import basic_router

from database.db_session import global_init
from middlewares.swarms import SwarmMiddleware


TG_BOT_TOKEN = getenv("TG_BOT_TOKEN")
OPENAI_API_KEY = getenv("OPENAI_API_KEY")
DB_USER = getenv("DB_USER", "root")
DB_PASSWORD = getenv("DB_PASSWORD", "password")
DB_HOST = getenv("DB_HOST", "localhost")
DB_PORT = getenv("DB_PORT", "3306")
DB_NAME = getenv("DB_NAME", "ai_interface")


async def main():
    logging.basicConfig(level=logging.INFO)
    
    # Инициализация базы данных
    global_init(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        delete_db=False  # Установите True, если нужно пересоздать таблицы
    )
    
    bot = Bot(token=TG_BOT_TOKEN)
    dp = Dispatcher()
    
    # Инициализация Swarm
    swarm_client = Swarm()

    # Подключаем middleware
    dp.update.middleware(SwarmMiddleware(swarm_client, OPENAI_API_KEY))
    
    # Подключение роутеров
    dp.include_router(voice_router)
    dp.include_router(commands_router)
    dp.include_router(basic_router)
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())