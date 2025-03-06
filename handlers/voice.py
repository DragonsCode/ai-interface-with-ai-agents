from aiogram import Router, F
from aiogram.types import Message
from swarm import Swarm
from database.db import Database
from agents.transcribe import voice_to_text
from agents.intent_agent import get_intent_agent

voice_router = Router()

@voice_router.message(F.content_type.in_(["voice", "audio"]))
async def voice_audio_handler(message: Message, swarm_client: Swarm, api_key: str):
    file = message.voice if message.voice else message.audio
    file_info = await message.bot.get_file(file.file_id)
    destination = f"voices/temp_{file_info.file_id}.wav"
    await message.bot.download_file(file_info.file_path, destination)

    agent = get_intent_agent()

    with Database() as db:
        history = db.get_history(message.from_user.id, limit=5)
    
    messages = []
    for user_msg, bot_resp in reversed(history):
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_resp})
    
    text = voice_to_text(destination, api_key)
    messages.append({"role": "user", "content": text})
    response = swarm_client.run(
        agent=agent,
        messages=messages,
        context_variables={"user_id": message.from_user.id}
    )
    await message.answer(f"{response.agent.name}: "+response.messages[-1]["content"], parse_mode="Markdown")