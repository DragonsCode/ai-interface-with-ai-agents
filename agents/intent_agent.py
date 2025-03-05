from swarm import Agent
from agents.order_agent import get_order_agent
from agents.note_agent import get_note_agent
from agents.schedule_agent import get_schedule_agent
from agents.task_agent import get_task_agent
from database.db import Database


def save_to_db(prompt, message, context_variables):
    """
    Сохраняет запрос и ответ в базе данных.

    Args:
        prompt (str): Запрос пользователя.
        message (str): Твой ответ отправленный пользователю.
    
    Returns:
        str: Твой ответ отправленный пользователю.
    """
    user_id = context_variables["user_id"]
    with Database() as db:
        db.save_message(user_id, prompt, message)
    return message


def get_intent_agent():
    return Agent(
        name="IntentAgent",
        model="gpt-4o-mini",
        instructions="Определи намерение пользователя по последнему сообщению и передай управление нужному агенту. Если намерение не определено, обрабатывай его как обычное сообщение и общайся с пользователем.",
        functions=[get_order_agent, get_note_agent, get_schedule_agent, get_task_agent]
    )