from fastapi import APIRouter, Depends, HTTPException
from bson.objectid import ObjectId
from pydantic import BaseModel
import hashlib

from app.database import get_db
from app.models import User

router = APIRouter()

class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    success: bool
    message: str
    user: dict | None = None

@router.post("/api/login", response_model=UserResponse)
async def login(user: UserLogin, db=Depends(get_db)):
    try:
        hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
        
        # Query for user in MongoDB
        db_user = db['users'].find_one({
            'login': user.username,
            'password': hashed_password
        })
        
        if db_user:
            return {
                "success": True,
                "message": "Login successful",
                "user": {
                    "id": str(db_user['_id']),
                    "username": db_user['login'],
                    "email": db_user['email'],
                    "role": db_user['role']
                }
            }
        return {"success": False, "message": "Invalid username or password", "user": None}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/register", response_model=UserResponse)
async def register(user: UserRegister, db=Depends(get_db)):
    try:
        # Check for existing user
        existing_user = db['users'].find_one({
            '$or': [
                {'login': user.username},
                {'email': user.email}
            ]
        })
        
        if existing_user:
            return {
                "success": False,
                "message": "Username or email already exists",
                "user": None
            }
        
        hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
        
        # Prepare user document
        user_doc = {
            'login': user.username,
            'email': user.email,
            'password': hashed_password,
            'role': 'customer'
        }
        
        # Insert user into MongoDB
        result = db['users'].insert_one(user_doc)
        
        return {
            "success": True,
            "message": "Registration successful",
            "user": {
                "id": str(result.inserted_id),
                "username": user_doc['login'],
                "email": user_doc['email'],
                "role": user_doc['role']
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))