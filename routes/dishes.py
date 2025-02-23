from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3

router = APIRouter()

class DishCreate(BaseModel):
    title: str
    description: str
    price: float

class DishUpdate(DishCreate):
    pass

def get_db():
    conn = sqlite3.connect('shop.db')
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

@router.post("/api/dishes")
async def create_dish(dish: DishCreate):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Insert new dish
        cursor.execute("""
            INSERT INTO Dishes (title, description, price)
            VALUES (?, ?, ?)
        """, (dish.title, dish.description, dish.price))
        
        conn.commit()
        
        return {
            "success": True,
            "message": "Dish created successfully",
            "id": cursor.lastrowid
        }
        
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@router.get("/api/dishes/{dish_id}")
async def get_dish(dish_id: int):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, description, price 
            FROM Dishes 
            WHERE id = ?
        """, (dish_id,))
        
        dish = cursor.fetchone()
        
        if not dish:
            raise HTTPException(status_code=404, detail="Dish not found")
            
        return {
            "id": dish[0],
            "title": dish[1],
            "description": dish[2],
            "price": dish[3]
        }
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@router.delete("/api/dishes/{dish_id}")
async def delete_dish(dish_id: int):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if dish exists
        cursor.execute("SELECT id FROM Dishes WHERE id = ?", (dish_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Dish not found")
            
        # Check if dish has any orders
        cursor.execute("SELECT COUNT(*) FROM Orders WHERE dish_id = ?", (dish_id,))
        order_count = cursor.fetchone()[0]
        
        if order_count > 0:
            return {
                "success": False,
                "message": "Cannot delete dish because it has existing orders"
            }
        
        # Delete dish if no orders exist
        cursor.execute("DELETE FROM Dishes WHERE id = ?", (dish_id,))
        conn.commit()
        
        return {
            "success": True,
            "message": "Dish deleted successfully"
        }
        
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        return {
            "success": False,
            "message": f"Database error: {str(e)}"
        }
    finally:
        if conn:
            conn.close()

@router.put("/api/dishes/{dish_id}")
async def update_dish(dish_id: int, dish: DishUpdate):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Verify dish exists
        cursor.execute("SELECT id FROM Dishes WHERE id = ?", (dish_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Dish not found")
        
        # Update dish
        cursor.execute("""
            UPDATE Dishes 
            SET title = ?, description = ?, price = ?
            WHERE id = ?
        """, (dish.title, dish.description, dish.price, dish_id))
        
        conn.commit()
        
        return {
            "success": True,
            "message": "Dish updated successfully"
        }
        
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()