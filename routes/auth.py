from fastapi import APIRouter
from fastapi.responses import JSONResponse, FileResponse
import sqlite3
import hashlib

router = APIRouter()

def get_db():
    try:
        conn = sqlite3.connect('shop.db')
        # Enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def init_db():
    conn = get_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Create User table with role column
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS User (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('admin', 'customer'))
                )
            """)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
        finally:
            conn.close()

# Initialize database
init_db()

@router.post("/api/login")
async def login(user: dict):
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        hashed_password = hashlib.sha256(user['password'].encode()).hexdigest()
        
        cursor.execute(
            "SELECT id, login, email, role FROM User WHERE login = ? AND password = ?",
            (user['username'], hashed_password)
        )
        user_data = cursor.fetchone()
        
        if user_data:
            return {
                "success": True, 
                "message": "Login successful",
                "user": {
                    "id": user_data[0],
                    "username": user_data[1],
                    "email": user_data[2],
                    "role": user_data[3]
                }
            }
        else:
            return {"success": False, "message": "Invalid username or password"}
        
    except sqlite3.Error as e:
        return {"success": False, "message": f"Database error: {str(e)}"}
    except Exception as e:
        return {"success": False, "message": "Server error"}
    finally:
        if conn:
            conn.close()

@router.post("/api/register")
async def register(user: dict):
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if username or email already exists
        cursor.execute("SELECT * FROM User WHERE login = ? OR email = ?",
                      (user['username'], user['email']))
        
        if cursor.fetchone():
            return {"success": False, "message": "Username or email already exists"}
        
        hashed_password = hashlib.sha256(user['password'].encode()).hexdigest()
        
        # Insert new user with role 'customer' by default
        cursor.execute(
            "INSERT INTO User (login, email, password, role) VALUES (?, ?, ?, ?)",
            (user['username'], user['email'], hashed_password, 'customer')
        )
        conn.commit()
        
        return {"success": True, "message": "Registration successful"}
        
    except sqlite3.Error as e:
        return {"success": False, "message": f"Database error: {str(e)}"}
    except Exception as e:
        print(f"Error during registration: {str(e)}")
        return {"success": False, "message": "Server error"}
    finally:
        if conn:
            conn.close()