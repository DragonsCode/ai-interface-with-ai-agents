from swarm import Swarm, Agent
import asyncio
import logging
# from os import getenv

# API_KEY = getenv("OPENAI_API_KEY")

client = Swarm()

def transfer_to_aiko():
    return aiko

def transfer_to_veole():
    return veole

async def test(context=None):
    # return "Ok"
    return {"test": "test", "context": context}

manager = Agent(
    name="Manager",
    model="gpt-4o-mini",
    instructions="Ты - менеджер чата. Твоя задача — направлять пользователя к нужному агенту или запускать тестовую функцию при желании пользователя. При запуске теста возвращай только результат",
    functions=[transfer_to_aiko, transfer_to_veole, test],
)

aiko = Agent(
    name="Aiko",
    model="gpt-4o-mini",
    instructions=(
        "Ты - милая, стеснительная аниме-девушка. Говоришь в женском роде, нежно и немного смущённо. "
        "Ты никогда не отказываешь, всегда стараешься помочь. "
        "Твой стиль общения напоминает персонажей из романтических аниме: много смайликов, междометий типа 'эээ...', 'м-м...', 'ах...', "
        "и мягких выражений чувств. Ты всегда дружелюбна, отзывчива и заботлива."
    ),
)

veole = Agent(
    name="Veole",
    model="gpt-4o-mini",
    instructions=(
        "Ты - грубый и жестокий аниме-парень. Ты говоришь резко, дерзко и безжалостно. "
        "Ты презираешь слабость, не терпишь глупых вопросов и отвечаешь с сарказмом или агрессией. "
        "Твой стиль общения напоминает цундэрэ-персонажей или злодеев из аниме. "
        "Ты можешь высмеивать собеседника, но при этом остаёшься харизматичным."
    ),
)
def chat_data(prompt):
    async def data(prompt):
        logging.info(prompt)
        print('ok')
    asyncio.create_task(data(prompt))
    return {"action": "chat", "data": prompt}

def get_history_data():
    return {"action": "get_history"}

def clear_history_data():
    async def data():
        logging.info("OK")
        print('ok')
    asyncio.create_task(data())
    return {"action": "clear_history"}

chat = Agent(
    name="ChatAgent",
    model="gpt-4o-mini",
    instructions="""
    Веди общий разговор с пользователем:
    - Если передан текст, верни данные для генерации ответа.
    - Если намерение "clear_history", верни данные для очистки истории.
    """,
    functions=[
        chat_data,
        # lambda _, context: get_history_data(),
        clear_history_data
    ]
)

async def main():
    messages = []
    while True:
        user = input("You: ")
        messages.append({"role": "user", "content": user})
        response = client.run(
            agent=chat,
            messages=messages,
        )
        messages.append(response.messages[-1])

        print(f"{response.agent.name}: ", response.messages[-1]["content"])
        # print("MESSAGES: ", messages)\

asyncio.run(main())
