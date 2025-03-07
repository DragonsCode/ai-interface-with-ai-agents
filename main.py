import asyncio
import logging
from swarm import Swarm
from aiogram import Bot, Dispatcher

from handlers.voice import voice_router
from handlers.commands import commands_router
from handlers.basic import basic_router

from config import TG_BOT_TOKEN, OPENAI_API_KEY, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, scheduler
from database.db_session import global_init
from middlewares.swarms import SwarmMiddleware



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

    # Запуск планировщика
    scheduler.start()
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())