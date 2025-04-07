from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from app.database import execute_query, get_db_cursor

router = APIRouter()

class DishBase(BaseModel):
    title: str
    description: str
    price: float

class DishCreate(DishBase):
    pass

class DishResponse(DishBase):
    id: int
    
    class Config:
        orm_mode = True

@router.post("/api/dishes", response_model=dict)
async def create_dish(dish: DishCreate):
    try:
        query = """
        INSERT INTO dishes (title, description, price)
        VALUES (%s, %s, %s)
        RETURNING id
        """
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(query, (dish.title, dish.description, dish.price))
            result = cursor.fetchone()
        
        return {
            "success": True,
            "message": "Dish created successfully",
            "id": result['id']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/dishes/{dish_id}", response_model=DishResponse)
async def get_dish(dish_id: int):
    query = "SELECT id, title, description, price FROM dishes WHERE id = %s"
    result = execute_query(query, (dish_id,))
    
    if not result or len(result) == 0:
        raise HTTPException(status_code=404, detail="Dish not found")
    
    return result[0]

@router.get("/api/dishes", response_model=dict)
async def get_dishes():
    query = "SELECT id, title, description, price FROM dishes"
    dishes = execute_query(query)
    
    return {
        "success": True,
        "dishes": dishes
    }

@router.delete("/api/dishes/{dish_id}")
async def delete_dish(dish_id: int):
    try:
        # Check if dish exists
        check_query = "SELECT id FROM dishes WHERE id = %s"
        dish = execute_query(check_query, (dish_id,))
        
        if not dish or len(dish) == 0:
            raise HTTPException(status_code=404, detail="Dish not found")
        
        # Check if dish has orders
        order_query = "SELECT COUNT(*) FROM order_items WHERE dish_id = %s"
        with get_db_cursor() as cursor:
            cursor.execute(order_query, (dish_id,))
            order_count = cursor.fetchone()['count']
        
        if order_count > 0:
            return {
                "success": False,
                "message": "Cannot delete dish because it has existing orders"
            }
        
        # Delete dish
        delete_query = "DELETE FROM dishes WHERE id = %s"
        execute_query(delete_query, (dish_id,), commit=True)
        
        return {
            "success": True,
            "message": "Dish deleted successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/api/dishes/{dish_id}")
async def update_dish(dish_id: int, dish_update: DishCreate):
    try:
        check_query = "SELECT id FROM dishes WHERE id = %s"
        dish = execute_query(check_query, (dish_id,))
        
        if not dish or len(dish) == 0:
            raise HTTPException(status_code=404, detail="Dish not found")
        
        update_query = """
        UPDATE dishes 
        SET title = %s, description = %s, price = %s
        WHERE id = %s
        """
        execute_query(
            update_query, 
            (dish_update.title, dish_update.description, dish_update.price, dish_id),
            commit=True
        )
        
        return {
            "success": True,
            "message": "Dish updated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))