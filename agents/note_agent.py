from swarm import Agent
from database.db import Database

def save_note(note_text: str, context_variables):
    """
    Сохраняет заметку пользователя.

    Args:
    note_text: Текст заметки.
    """
    user_id = context_variables["user_id"]
    with Database() as db:
        db.save_note(user_id, note_text)
    return f"Заметка сохранена: {note_text}"

def get_notes(context_variables):
    """Возвращает список заметок пользователя."""
    user_id = context_variables["user_id"]
    with Database() as db:
        notes = db.get_notes(user_id)
        if not notes:
            return "У вас пока нет заметок."
        return "\n".join(f"Заметка {note_id}: {note_text}" for note_id, note_text in notes)

def clear_notes(context_variables):
    """Очищает все заметки пользователя."""
    user_id = context_variables["user_id"]
    with Database() as db:
        db.clear_notes(user_id)
    return "Все заметки очищены."

def get_note_agent():
    """Этот агент отвечает за управление заметками."""
    return Agent(
        name="NoteAgent",
        model="gpt-4o-mini",
        instructions="Управляй заметками: сохраняй, показывай или очищай их.",
        functions=[save_note, get_notes, clear_notes]
    )