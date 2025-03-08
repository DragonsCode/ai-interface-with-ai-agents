from sqlalchemy import select
from datetime import datetime
from typing import List, Tuple

from .db_session import create_session
from .base_db_api import BaseDBApi
from .models.history import History
from .models.order import Order
from .models.order_item import OrderItem
from .models.note import Note
from .models.schedule import Schedule
from .models.task import Task
from .models.menu import Menu

class Database(BaseDBApi):
    def save_message(self, user_id: int, message: str, response: str):
        history = History(user_id=user_id, message=message, response=response)
        self._sess.add(history)
        self._sess.commit()

    def get_history(self, user_id: int, limit: int = 5) -> List[Tuple[str, str]]:
        result = self._sess.execute(
            select(History)
            .where(History.user_id == user_id)
            .order_by(History.timestamp.desc())
            .limit(limit)
        )
        history = result.scalars().all()
        return [(h.message, h.response) for h in history]

    def clear_history(self, user_id: int):
        self._sess.execute(
            History.__table__.delete().where(History.user_id == user_id)
        )
        self._sess.commit()

    def save_order(self, user_id: int, order_items: List[Tuple[int, int]]):
        order = Order(user_id=user_id)
        self._sess.add(order)
        self._sess.flush()  # Получаем order.id
        for menu_id, quantity in order_items:
            order_item = OrderItem(order_id=order.id, menu_id=menu_id, quantity=quantity)
            self._sess.add(order_item)
        self._sess.commit()

    def get_orders(self, user_id: int) -> List[Tuple[int, List[Tuple[int, str, int]]]]:
        result = self._sess.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .order_by(Order.timestamp.desc())
        )
        orders = result.scalars().all()
        orders_list = []
        for order in orders:
            items_result = self._sess.execute(
                select(OrderItem)
                .where(OrderItem.order_id == order.id)
            )
            items = items_result.scalars().all()
            orders_list.append((order.id, [(item.id, item.menu_id, item.quantity) for item in items]))
        return orders_list

    def clear_orders(self, user_id: int):
        orders_result = self._sess.execute(
            select(Order)
            .where(Order.user_id == user_id)
        )
        orders = orders_result.scalars().all()
        for order in orders:
            self._sess.execute(
                OrderItem.__table__.delete().where(OrderItem.order_id == order.id)
            )
        self._sess.execute(
            Order.__table__.delete().where(Order.user_id == user_id)
        )
        self._sess.commit()

    def save_note(self, user_id: int, note_text: str):
        note = Note(user_id=user_id, note_text=note_text)
        self._sess.add(note)
        self._sess.commit()

    def get_notes(self, user_id: int) -> List[Tuple[int, str]]:
        result = self._sess.execute(
            select(Note)
            .where(Note.user_id == user_id)
            .order_by(Note.timestamp.desc())
        )
        notes = result.scalars().all()
        return [(note.id, note.note_text) for note in notes]

    def clear_notes(self, user_id: int):
        self._sess.execute(
            Note.__table__.delete().where(Note.user_id == user_id)
        )
        self._sess.commit()

    def save_event(self, user_id: int, event_text: str, event_datetime: str):
        event = Schedule(user_id=user_id, event_text=event_text, event_datetime=event_datetime)
        self._sess.add(event)
        self._sess.commit()

    def get_events(self, user_id: int) -> List[Tuple[int, str, str]]:
        result = self._sess.execute(
            select(Schedule)
            .where(Schedule.user_id == user_id)
            .order_by(Schedule.event_datetime.asc())
        )
        events = result.scalars().all()
        return [(event.id, event.event_text, event.event_datetime) for event in events]

    def clear_events(self, user_id: int):
        self._sess.execute(
            Schedule.__table__.delete().where(Schedule.user_id == user_id)
        )
        self._sess.commit()

    def save_task(self, user_id: int, task_text: str, deadline: str):
        task = Task(user_id=user_id, task_text=task_text, deadline=deadline)
        self._sess.add(task)
        self._sess.commit()

    def get_tasks(self, user_id: int, only_open: bool = True) -> List[Tuple[int, str, str, bool]]:
        query = select(Task).where(Task.user_id == user_id)
        if only_open:
            query = query.where(Task.is_done == False)
        result = self._sess.execute(query.order_by(Task.deadline.asc()))
        tasks = result.scalars().all()
        return [(task.id, task.task_text, task.deadline, task.is_done) for task in tasks]

    def mark_task_done(self, user_id: int, task_id: int):
        task = self._sess.get(Task, task_id)
        if task and task.user_id == user_id:
            task.is_done = True
            self._sess.commit()

    def clear_tasks(self, user_id: int):
        self._sess.execute(
            Task.__table__.delete().where(Task.user_id == user_id)
        )
        self._sess.commit()
    
    def get_menu(self) -> List[Tuple[int, str, str, str, bool]]:
        result = self._sess.execute(
            select(Menu)
            .order_by(Menu.name.asc())
        )
        menu = result.scalars().all()
        return [(item.id, item.name, item.description, str(item.price) + " UZS", item.is_available) for item in menu]