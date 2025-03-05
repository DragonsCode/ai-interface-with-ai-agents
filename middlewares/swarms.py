from aiogram.types import Message
from aiogram.dispatcher.middlewares.base import BaseMiddleware

class SwarmMiddleware(BaseMiddleware):
    def __init__(self, swarm_client, api_key):
        super().__init__()
        self.swarm_client = swarm_client
        self.api_key = api_key

    async def __call__(self, handler, event: Message, data: dict):
        # Передаем swarm_client и api_key в data, откуда их получит хендлер
        data["swarm_client"] = self.swarm_client
        data["api_key"] = self.api_key
        return await handler(event, data)
