from database.db import Database
from openai import OpenAI
import logging


def get_answer(user_id: int, prompt: str, api_key: str) -> str:
    """
    Делает запрос к API OpenAI и возвращает ответ от GPT-4o-mini с учетом истории чата.
    Используется для обычного диалога.

    Args:
        user_id (int): Идентификатор пользователя.
        prompt (str): Сообщение пользователя.
        api_key (str): Ключ API OpenAI.

    Returns:
        str: Ответ от GPT-4o-mini.
    """
    try:
        client = OpenAI(api_key=api_key)
        
        with Database() as db:
            history = db.get_history(user_id)
        messages = [{"role": "system", "content": "Ты милый ассистент."}]
        for user_msg, bot_resp in reversed(history):
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": bot_resp})
        
        messages.append({"role": "user", "content": prompt})
        
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        
        response_text = completion.choices[0].message.content.strip()
        return response_text
    except Exception as e:
        logging.error(f"Ошибка в get_answer: {e}")
        return "Извините, произошла ошибка при обработке вашего запроса."