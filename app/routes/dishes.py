from fastapi import APIRouter, Depends, HTTPException
from bson.objectid import ObjectId
from pydantic import BaseModel
from typing import List, Dict, Any

from app.database import get_db

router = APIRouter()

class DishBase(BaseModel):
    title: str
    description: str
    price: float

class DishCreate(DishBase):
    pass

class DishResponse(DishBase):
    id: str
    
    class Config:
        orm_mode = True

@router.post("/api/dishes", response_model=dict)
async def create_dish(dish: DishCreate, db=Depends(get_db)):
    try:
        # Prepare dish document
        dish_doc = {
            'title': dish.title,
            'description': dish.description,
            'price': dish.price
        }
        
        # Insert dish into MongoDB
        result = db['dishes'].insert_one(dish_doc)
        
        return {
            "success": True,
            "message": "Dish created successfully",
            "id": str(result.inserted_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/dishes/{dish_id}", response_model=DishResponse)
async def get_dish(dish_id: str, db=Depends(get_db)):
    # Find dish by ObjectId
    dish = db['dishes'].find_one({'_id': ObjectId(dish_id)})
    
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    
    # Convert ObjectId to string for response
    dish['id'] = str(dish['_id'])
    return dish

@router.get("/api/dishes", response_model=dict)
async def get_dishes(db=Depends(get_db)):
    # Fetch all dishes
    dishes = list(db['dishes'].find())
    
    # Convert ObjectId to string and prepare response
    formatted_dishes = []
    for dish in dishes:
        formatted_dish = {
            "id": str(dish['_id']),
            "title": dish['title'],
            "description": dish['description'],
            "price": dish['price']
        }
        formatted_dishes.append(formatted_dish)
    
    return {
        "success": True,
        "dishes": formatted_dishes
    }

@router.delete("/api/dishes/{dish_id}")
async def delete_dish(dish_id: str, db=Depends(get_db)):
    try:
        # Check if dish exists
        dish = db['dishes'].find_one({'_id': ObjectId(dish_id)})
        if not dish:
            raise HTTPException(status_code=404, detail="Dish not found")
        
        # Check for existing orders
        order_count = db['orders'].count_documents({'dish_id': dish_id})
        if order_count > 0:
            return {
                "success": False,
                "message": "Cannot delete dish because it has existing orders"
            }
        
        # Delete the dish
        db['dishes'].delete_one({'_id': ObjectId(dish_id)})
        
        return {
            "success": True,
            "message": "Dish deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/api/dishes/{dish_id}")
async def update_dish(dish_id: str, dish_update: DishCreate, db=Depends(get_db)):
    try:
        # Check if dish exists
        dish = db['dishes'].find_one({'_id': ObjectId(dish_id)})
        if not dish:
            raise HTTPException(status_code=404, detail="Dish not found")
        
        # Prepare update document
        update_doc = {
            'title': dish_update.title,
            'description': dish_update.description,
            'price': dish_update.price
        }
        
        # Update the dish
        db['dishes'].update_one(
            {'_id': ObjectId(dish_id)}, 
            {'$set': update_doc}
        )
        
        return {
            "success": True,
            "message": "Dish updated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))