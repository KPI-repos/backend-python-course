from fastapi import APIRouter, Depends, HTTPException
from bson.objectid import ObjectId
from pydantic import BaseModel
from datetime import datetime

from app.database import get_db

router = APIRouter()

class OrderCreate(BaseModel):
    userId: str
    dishId: str

@router.post("/api/orders")
async def create_order(order: OrderCreate, db=Depends(get_db)):
    try:
        # Verify user exists and is a customer
        user = db['users'].find_one({
            '_id': ObjectId(order.userId),
            'role': 'customer'
        })
        if not user:
            raise HTTPException(status_code=404, detail="User not found or not authorized")

        # Verify dish exists
        dish = db['dishes'].find_one({'_id': ObjectId(order.dishId)})
        if not dish:
            raise HTTPException(status_code=404, detail="Dish not found")

        # Prepare order document
        order_doc = {
            'user_id': order.userId,
            'dish_id': order.dishId,
            'status': 'pending',
            'created_at': datetime.now()
        }
        
        # Insert order into MongoDB
        result = db['orders'].insert_one(order_doc)
        
        return {
            "success": True,
            "message": "Order created successfully",
            "id": str(result.inserted_id)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))