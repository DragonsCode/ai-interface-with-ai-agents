from aiogram import Router
from aiogram.types import Message
from swarm import Swarm
from database.db import Database
from agents.intent_agent import get_intent_agent, save_to_db

basic_router = Router()



@basic_router.message()
async def messages_handler(message: Message, swarm_client: Swarm):
    agent = get_intent_agent()

    with Database() as db:
        history = db.get_history(message.from_user.id, limit=5)
    
    messages = []
    for user_msg, bot_resp in reversed(history):
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_resp})
    messages.append({"role": "user", "content": message.text})

    response = swarm_client.run(
        agent=agent,
        messages=messages,
        context_variables={"user_id": message.from_user.id}
    )

    save_to_db(message.text, response.messages[-1]["content"], {"user_id": message.from_user.id})
    await message.answer(f"{response.agent.name}: "+response.messages[-1]["content"])