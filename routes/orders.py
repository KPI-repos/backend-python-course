from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3
from datetime import datetime

router = APIRouter()

class OrderCreate(BaseModel):
    userId: int
    dishId: int

def get_db():
    conn = sqlite3.connect('shop.db')
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

@router.post("/api/orders")
async def create_order(order: OrderCreate):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Verify user exists and is a customer
        cursor.execute("SELECT role FROM User WHERE id = ? AND role = 'customer'", (order.userId,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found or not authorized")

        # Verify dish exists
        cursor.execute("SELECT id FROM Dishes WHERE id = ?", (order.dishId,))
        dish = cursor.fetchone()
        if not dish:
            raise HTTPException(status_code=404, detail="Dish not found")

        # Create the order
        cursor.execute("""
            INSERT INTO Orders (user_id, dish_id, status, created_at)
            VALUES (?, ?, 'pending', ?)
        """, (order.userId, order.dishId, datetime.now().isoformat()))
        
        conn.commit()
        
        return {
            "success": True,
            "message": "Order created successfully"
        }

    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if conn:
            conn.close()

@router.get("/api/dishes")
async def get_dishes():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, title, description, price FROM Dishes")
        dishes = cursor.fetchall()
        
        return {
            "success": True,
            "dishes": [
                {
                    "id": dish[0],
                    "title": dish[1],
                    "description": dish[2],
                    "price": dish[3]
                }
                for dish in dishes
            ]
        }

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if conn:
            conn.close()