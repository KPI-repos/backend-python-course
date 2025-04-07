from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import hashlib
from typing import Optional

from app.database import execute_query, get_db_cursor

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
    user: Optional[dict] = None

@router.post("/api/login", response_model=UserResponse)
async def login(user: UserLogin):
    try:
        hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
        
        query = """
        SELECT id, login, email, role 
        FROM users 
        WHERE login = %s AND password = %s
        """
        
        result = execute_query(query, (user.username, hashed_password))
        
        if result and len(result) > 0:
            db_user = result[0]
            return {
                "success": True,
                "message": "Login successful",
                "user": {
                    "id": db_user['id'],
                    "username": db_user['login'],
                    "email": db_user['email'],
                    "role": db_user['role']
                }
            }
        return {"success": False, "message": "Invalid username or password", "user": None}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/register", response_model=UserResponse)
async def register(user: UserRegister):
    try:
        # Check if username or email already exists
        check_query = """
        SELECT id FROM users
        WHERE login = %s OR email = %s
        """
        existing_user = execute_query(check_query, (user.username, user.email))
        
        if existing_user and len(existing_user) > 0:
            return {
                "success": False,
                "message": "Username or email already exists",
                "user": None
            }
        
        hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
        
        # Insert new user
        insert_query = """
        INSERT INTO users (login, email, password, role)
        VALUES (%s, %s, %s, %s)
        RETURNING id, login, email, role
        """
        
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(insert_query, (user.username, user.email, hashed_password, 'customer'))
            db_user = cursor.fetchone()
        
        return {
            "success": True,
            "message": "Registration successful",
            "user": {
                "id": db_user['id'],
                "username": db_user['login'],
                "email": db_user['email'],
                "role": db_user['role']
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))