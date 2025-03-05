from swarm import Agent
from database.db import Database
from datetime import datetime
import json

def save_event(event_data, context_variables):
    """
    Сохраняет событие в расписании.

    Args:
    event_data: Строка с данными о событии в формате JSON. Пример:
    {"event_text": "Событие 1", "event_datetime": "2023-09-01T10:00:00"}
    """
    user_id = context_variables["user_id"]
    try:
        data = json.loads(event_data)
        event_text = data["event_text"]
        event_datetime = data["event_datetime"]
        with Database() as db:
            db.save_event(user_id, event_text, event_datetime)
        return f"Событие '{event_text}' добавлено на {event_datetime}."
    except Exception as e:
        return f"Ошибка: {str(e)}. Укажите событие и время в формате 'YYYY-MM-DDTHH:MM:SS'."

def get_events(context_variables):
    """Возвращает список событий пользователя."""
    user_id = context_variables["user_id"]
    with Database() as db:
        events = db.get_events(user_id)
        if not events:
            return "У вас нет событий."
        return "\n".join(f"Событие {event_id}: '{event_text}' на {event_datetime}" 
                         for event_id, event_text, event_datetime in events)

def clear_events(context_variables):
    """Очищает все события пользователя."""
    user_id = context_variables["user_id"]
    with Database() as db:
        db.clear_events(user_id)
    return "Все события очищены."

def get_schedule_agent():
    now = datetime.now()
    return Agent(
        name="ScheduleAgent",
        model="gpt-4o-mini",
        instructions=f"Управляй расписанием: сохраняй, показывай или очищай события. Можешь так же получить события и сообщить опаздывает ли пользователь по расписанию. Сейчас время: {now.strftime('%Y-%m-%d %H:%M:%S')}.",
        functions=[save_event, get_events, clear_events]
    )