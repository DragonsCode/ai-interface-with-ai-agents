from .intent_agent import get_intent_agent
from .order_agent import get_order_agent
from .note_agent import get_note_agent
from .schedule_agent import get_schedule_agent
from .task_agent import get_task_agent

def get_all_agents():
    return [
        get_intent_agent(),
        get_order_agent(),
        get_note_agent(),
        get_schedule_agent(),
        get_task_agent(),
    ]