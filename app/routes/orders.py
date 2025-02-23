from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from app.database import get_db
from app.models import Order, User, Dish

router = APIRouter()

class OrderCreate(BaseModel):
    userId: int
    dishId: int

@router.post("/api/orders")
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(
            User.id == order.userId,
            User.role == 'customer'
        ).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found or not authorized")

        dish = db.query(Dish).filter(Dish.id == order.dishId).first()
        if not dish:
            raise HTTPException(status_code=404, detail="Dish not found")

        db_order = Order(
            user_id=order.userId,
            dish_id=order.dishId,
            status='pending',
            created_at=datetime.now()
        )
        
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        return {
            "success": True,
            "message": "Order created successfully",
            "id": db_order.id
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))