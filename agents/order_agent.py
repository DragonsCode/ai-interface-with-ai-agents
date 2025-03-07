from swarm import Agent
from database.db import Database
import json


def get_menu(context_variables):
    """
    Возвращает меню.
    
    Returns:
    menu: меню доступных товаров в формате [(id, name, description, price, is_available)]
    Пример:
    [(1, "Товар 1", "Описание товара 1", "10000.0 UZS", False), (2, "Товар 2", "Описание товара 2", "24999.99 UZS", True)]
    """
    with Database() as db:
        menu = db.get_menu()
    return str(menu)

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
    """Этот агент отвечает за обработку заказов и показа меню товаров."""
    return Agent(
        name="OrderAgent",
        model="gpt-4o-mini",
        instructions="""
Ты отвечаешь за обработку заказов в кафе. Работай строго с меню, не предлагай товары, которых нет в базе данных. Валюта: узбекский сум.
1. **Получение меню**: Перед тем как обработать заказ, всегда сначала вызывай `get_menu()`, чтобы убедиться, что запрашиваемые товары доступны.
2. **Обработка заказа**: Если все товары есть в наличии, вызывай `process_order()` и подтверждай заказ.
3. **Отсутствие товаров**: Если какого-то товара нет, не принимай заказ сразу, а предложи замену или похожий вариант из меню.
4. **Просмотр заказов**: Если пользователь хочет увидеть свои заказы, вызывай `get_orders()`.
5. **Очистка заказов**: Если пользователь хочет удалить все заказы, вызывай `clear_orders()`.

Будь настойчивым: если товар отсутствует, предложи похожий вариант или комбинацию доступных товаров. Не допускай оформления заказа с несуществующими позициями.
        """,
        functions=[get_menu, process_order, get_orders, clear_orders]
    )