from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBasic
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import sqlite3
import hashlib
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": str(exc.detail)}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"success": False, "message": "Invalid input data"}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal server error"}
    )

def get_db():
    try:
        conn = sqlite3.connect('example.db')
        return conn
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail="Database connection error")

@app.post("/api/login")
async def login(user: dict):
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        hashed_password = hashlib.sha256(user['password'].encode()).hexdigest()
        
        cursor.execute(
            "SELECT * FROM User WHERE login = ? AND password = ?",
            (user['username'], hashed_password)
        )
        user_data = cursor.fetchone()
        
        if user_data:
            return {"success": True, "message": "Login successful"}
        else:
            return {"success": False, "message": "Invalid username or password"}
            
    except sqlite3.Error as e:
        return {"success": False, "message": f"Database error: {str(e)}"}
    except Exception as e:
        return {"success": False, "message": "Server error"}
    finally:
        if conn:
            conn.close()

@app.post("/api/register")
async def register(user: dict):
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute("SELECT * FROM User WHERE login = ? OR email = ?", 
                      (user['username'], user['email']))
        
        if cursor.fetchone():
            return {"success": False, "message": "Username or email already exists"}
        
        # Hash the password
        hashed_password = hashlib.sha256(user['password'].encode()).hexdigest()
        
        # Insert new user
        cursor.execute(
            "INSERT INTO User (login, email, password) VALUES (?, ?, ?)",
            (user['username'], user['email'], hashed_password)
        )
        conn.commit()
        
        return {"success": True, "message": "Registration successful"}
            
    except sqlite3.Error as e:
        return {"success": False, "message": f"Database error: {str(e)}"}
    except Exception as e:
        print(f"Error during registration: {str(e)}")  # For debugging
        return {"success": False, "message": "Server error"}
    finally:
        if conn:
            conn.close()

# Static file routes
@app.get("/")
def read_root():
    return FileResponse('public/index.html')

@app.get("/login")
def read_login():
    return FileResponse('public/auth/login.html')

@app.get("/register")
def read_register():
    return FileResponse('public/auth/register.html')

@app.get("/menu")
def read_menu():
    return FileResponse('public/menu.html')