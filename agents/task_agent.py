from swarm import Agent
from database.db import Database
from datetime import datetime
import json
import requests

from config import TG_BOT_TOKEN, scheduler


def send_reminder(user_id, task_text):
    """Функция для отправки напоминания."""
    url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': user_id,
        'text': f"Напоминание о вашей задаче:\n{task_text}"
    }
    requests.post(url, json=data)

def schedule_reminder(user_id, task_text, reminder_time):
    """Запланировать напоминание в указанное агентом время."""
    try:
        reminder_time_dt = datetime.fromisoformat(reminder_time)
        now = datetime.now()

        if reminder_time_dt > now:
            scheduler.add_job(
                send_reminder,
                'date',
                run_date=reminder_time_dt,
                args=[user_id, task_text]
            )
            return f"Напоминание запланировано на {reminder_time_dt.strftime('%Y-%m-%d %H:%M:%S')}."
        return "Напоминание не установлено, так как дедлайн в прошлом."
    except ValueError:
        return "Ошибка: некорректный формат времени напоминания."

def save_task(task_data, context_variables):
    """
    Сохраняет задачу пользователя и устанавливает напоминание.

    Args:
    task_data: JSON-строка с задачей. reminder_time должен быть как минимум на час раньеше чем deadline и максимум на день. Пример:
    {"task_text": "Задача 1", "deadline": "2023-09-01T10:00:00", "reminder_time": "2023-09-01T07:00:00"}
    """
    user_id = context_variables["user_id"]
    try:
        data = json.loads(task_data)
        task_text = data["task_text"]
        deadline = data["deadline"]
        reminder_time = data.get("reminder_time")  # Может быть None

        with Database() as db:
            db.save_task(user_id, task_text, deadline)

        # Если ИИ передал время напоминания — запланировать
        reminder_msg = schedule_reminder(user_id, task_text, reminder_time) if reminder_time else "Напоминание не запланировано."

        return f"Задача '{task_text}' добавлена с дедлайном {deadline}.\n{reminder_msg}"
    except Exception as e:
        return f"Ошибка: {str(e)}. Укажите задачу и дедлайн в формате 'YYYY-MM-DDTHH:MM:SS'."

def get_tasks(only_open: bool, context_variables):
    """
    Возвращает список задач пользователя.
    
    Args:
    only_open: Если True, то возвращает только открытые задачи, иначе - все задачи.
    """
    user_id = context_variables["user_id"]
    with Database() as db:
        tasks = db.get_tasks(user_id, only_open)
        if not tasks:
            return "У вас нет задач."
        return "\n".join(f"Задача {task_id}: '{task_text}', ID задачи: {task_id}, дедлайн: {deadline} ({'Выполнена' if is_done else 'Открыта'})" 
                         for task_id, task_text, deadline, is_done in tasks)

def mark_task_done(task_id: int, context_variables):
    """
    Отмечает задачу как выполненную.
    
    Args:
    task_id: ID задачи.
    """
    user_id = context_variables["user_id"]
    try:
        task_id = int(task_id)
        with Database() as db:
            db.mark_task_done(user_id, task_id)
        return f"Задача {task_id} отмечена как выполненная."
    except ValueError:
        return "Ошибка: укажите корректный номер задачи."

def clear_tasks(context_variables):
    """Очищает все задачи пользователя."""
    user_id = context_variables["user_id"]
    with Database() as db:
        db.clear_tasks(user_id)
    return "Все задачи очищены."

def get_task_agent():
    """Этот агент отвечает за управление задачами."""
    now = datetime.now()
    return Agent(
        name="TaskAgent",
        model="gpt-4o-mini",
        instructions=f"Управляй задачами: сохраняй, показывай, отмечай выполненными или очищай. Можешь так же получить задачи и сообщить опаздывает ли пользователь по задачам. Сейчас время: {now.strftime('%Y-%m-%d %H:%M:%S')}.",
        functions=[save_task, get_tasks, mark_task_done, clear_tasks]
    )