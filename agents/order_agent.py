from swarm import Agent
from database.db import Database
import json

def process_order(order_data: list[dict], context_variables):
    """
    Сохраняет заказ в базе данных и возвращает подтверждение.

    Args:
    order_data: список, содержащий информацию о заказе. в формате 
    [{"name": "Товар 1", "quantity": 2}, {"name": "Товар 2", "quantity": 3}]
    """
    user_id = context_variables["user_id"]
    try:
        data = json.loads(order_data)
        items = [(item["name"], item["quantity"]) for item in data]
        with Database() as db:
            db.save_order(user_id, items)
        items_str = ", ".join(f"{qty} x {name}" for name, qty in items)
        return f"Заказ успешно принят: {items_str}"
    except Exception as e:
        return f"Ошибка: {str(e)}. Укажите товары и их количество."

def get_orders(context_variables):
    """Возвращает список заказов пользователя."""
    user_id = context_variables["user_id"]
    with Database() as db:
        orders = db.get_orders(user_id)
        if not orders:
            return "У вас пока нет заказов."
        response_lines = ["Ваши заказы:"]
        for order_id, items in orders:
            items_str = ", ".join(f"{qty} x {name}" for _, name, qty in items)
            response_lines.append(f"Заказ ID {order_id}: {items_str}")
        return "\n".join(response_lines)

def clear_orders(context_variables):
    """Очищает все заказы пользователя."""
    user_id = context_variables["user_id"]
    with Database() as db:
        db.clear_orders(user_id)
    return "Все заказы очищены."

def get_order_agent():
    return Agent(
        name="OrderAgent",
        model="gpt-4o-mini",
        instructions="Обрабатывай заказы: сохраняй их в базе данных или показывай список.",
        functions=[process_order, get_orders, clear_orders]
    )