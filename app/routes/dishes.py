from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.database import get_db
from app.models import Dish, Order

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
async def create_dish(dish: DishCreate, db: Session = Depends(get_db)):
    try:
        db_dish = Dish(**dish.dict())
        db.add(db_dish)
        db.commit()
        db.refresh(db_dish)
        
        return {
            "success": True,
            "message": "Dish created successfully",
            "id": db_dish.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/dishes/{dish_id}", response_model=DishResponse)
async def get_dish(dish_id: int, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish

@router.get("/api/dishes", response_model=dict)
async def get_dishes(db: Session = Depends(get_db)):
    dishes = db.query(Dish).all()
    return {
        "success": True,
        "dishes": [
            {
                "id": dish.id,
                "title": dish.title,
                "description": dish.description,
                "price": dish.price
            }
            for dish in dishes
        ]
    }

@router.delete("/api/dishes/{dish_id}")
async def delete_dish(dish_id: int, db: Session = Depends(get_db)):
    try:
        dish = db.query(Dish).filter(Dish.id == dish_id).first()
        if not dish:
            raise HTTPException(status_code=404, detail="Dish not found")
            
        order_count = db.query(Order).filter(Order.dish_id == dish_id).count()
        if order_count > 0:
            return {
                "success": False,
                "message": "Cannot delete dish because it has existing orders"
            }
        
        db.delete(dish)
        db.commit()
        
        return {
            "success": True,
            "message": "Dish deleted successfully"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/api/dishes/{dish_id}")
async def update_dish(dish_id: int, dish_update: DishCreate, db: Session = Depends(get_db)):
    try:
        dish = db.query(Dish).filter(Dish.id == dish_id).first()
        if not dish:
            raise HTTPException(status_code=404, detail="Dish not found")
        
        for key, value in dish_update.dict().items():
            setattr(dish, key, value)
            
        db.commit()
        db.refresh(dish)
        
        return {
            "success": True,
            "message": "Dish updated successfully"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))