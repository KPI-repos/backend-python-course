from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
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
async def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
        
        db_user = db.query(User).filter(
            User.login == user.username,
            User.password == hashed_password
        ).first()
        
        if db_user:
            return {
                "success": True,
                "message": "Login successful",
                "user": {
                    "id": db_user.id,
                    "username": db_user.login,
                    "email": db_user.email,
                    "role": db_user.role
                }
            }
        return {"success": False, "message": "Invalid username or password", "user": None}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/register", response_model=UserResponse)
async def register(user: UserRegister, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(
            (User.login == user.username) | (User.email == user.email)
        ).first()
        
        if existing_user:
            return {
                "success": False,
                "message": "Username or email already exists",
                "user": None
            }
        
        hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
        
        db_user = User(
            login=user.username,
            email=user.email,
            password=hashed_password,
            role='customer'
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return {
            "success": True,
            "message": "Registration successful",
            "user": {
                "id": db_user.id,
                "username": db_user.login,
                "email": db_user.email,
                "role": db_user.role
            }
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))