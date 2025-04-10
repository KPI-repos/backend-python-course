from typing import Optional, List, Dict, Any
from datetime import datetime
from bson.objectid import ObjectId

class User:
    """
    User model for MongoDB, mimicking SQLAlchemy User model structure
    """
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        """
        Initialize a User instance
        
        :param data: Dictionary containing user data
        """
        data = data or {}
        
        self._id = data.get('_id', ObjectId())
        
        self.login = data.get('login', '')
        self.email = data.get('email', '')
        self.password = data.get('password', '')
        
 
        role = data.get('role', 'customer')
        self.role = role if role in ['admin', 'customer'] else 'customer'
        
        self.orders: List[Dict] = data.get('orders', [])

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the model to a dictionary representation
        
        :return: Dictionary representation of the model
        """
        return {
            '_id': str(self._id),
            'login': self.login,
            'email': self.email,
            'password': self.password,
            'role': self.role,
            'orders': self.orders
        }

class Dish:
    """
    Dish model for MongoDB, mimicking SQLAlchemy Dish model structure
    """
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        """
        Initialize a Dish instance
        
        :param data: Dictionary containing dish data
        """
        data = data or {}
        
        # Preserve ObjectId if provided, otherwise generate a new one
        self._id = data.get('_id', ObjectId())
        
        # Required fields
        self.title = data.get('title', '')
        self.description = data.get('description', '')
        self.price = float(data.get('price', 0.0))
        
        # Relationship-like attribute (will be populated during queries)
        self.orders: List[Dict] = data.get('orders', [])

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the model to a dictionary representation
        
        :return: Dictionary representation of the model
        """
        return {
            '_id': str(self._id),
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'orders': self.orders
        }

class Order:
    """
    Order model for MongoDB, mimicking SQLAlchemy Order model structure
    """
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        """
        Initialize an Order instance
        
        :param data: Dictionary containing order data
        """
        data = data or {}
        
        self._id = data.get('_id', ObjectId())
        
        self.user_id = data.get('user_id')
        self.dish_id = data.get('dish_id')
        
        self.status = data.get('status', 'pending')
        self.created_at = data.get('created_at', datetime.utcnow())
        
        self.user: Optional[Dict] = data.get('user')
        self.dish: Optional[Dict] = data.get('dish')

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the model to a dictionary representation
        
        :return: Dictionary representation of the model
        """
        return {
            '_id': str(self._id),
            'user_id': self.user_id,
            'dish_id': self.dish_id,
            'status': self.status,
            'created_at': self.created_at,
            'user': self.user,
            'dish': self.dish
        }

__all__ = ['User', 'Dish', 'Order']