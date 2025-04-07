from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

from app.database import execute_query, get_db_cursor

router = APIRouter()

class OrderCreate(BaseModel):
    userId: int
    dishId: int

@router.post("/api/orders")
async def create_order(order: OrderCreate):
    try:
        user_query = """
        SELECT id FROM users 
        WHERE id = %s AND role = 'customer'
        """
        user = execute_query(user_query, (order.userId,))
        
        if not user or len(user) == 0:
            raise HTTPException(status_code=404, detail="User not found or not authorized")

        dish_query = "SELECT id FROM dishes WHERE id = %s"
        dish = execute_query(dish_query, (order.dishId,))
        
        if not dish or len(dish) == 0:
            raise HTTPException(status_code=404, detail="Dish not found")

        order_query = """
        INSERT INTO orders (user_id, status, created_at)
        VALUES (%s, %s, %s)
        RETURNING id
        """
        
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                order_query, 
                (order.userId, 'pending', datetime.now())
            )
            new_order = cursor.fetchone()
            
            order_item_query = """
            INSERT INTO order_items (order_id, dish_id, quantity, price)
            SELECT %s, %s, 1, price FROM dishes WHERE id = %s
            """
            cursor.execute(
                order_item_query,
                (new_order['id'], order.dishId, order.dishId)
            )
        
        return {
            "success": True,
            "message": "Order created successfully",
            "id": new_order['id']
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))