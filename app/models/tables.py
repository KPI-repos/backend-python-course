from dataclasses import dataclass
from datetime import datetime
from typing import Optional

class User:
    def __init__(self, id=None, login="", email="", password="", role="customer"):
        self.id = id
        self.login = login
        self.email = email
        self.password = password
        self.role = role

class Dish:
    def __init__(self, id=None, title="", description="", price=0.0):
        self.id = id
        self.title = title
        self.description = description
        self.price = price

class Order:
    def __init__(self, id=None, user_id=None, dish_id=None, status="pending", created_at=None):
        self.id = id
        self.user_id = user_id
        self.dish_id = dish_id
        self.status = status
        self.created_at = created_at if created_at else datetime.now()