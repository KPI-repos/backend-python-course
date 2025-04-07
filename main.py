from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from app.routes import auth_router, dishes_router, orders_router, pages_router

from app.database import get_db_connection

app = FastAPI(
    title="Restaurant API",
    description="API for restaurant management system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="public/static"), name="static")

try:
    with get_db_connection() as conn:
        print("Successfully connected to PostgreSQL database")
except Exception as e:
    print(f"Error connecting to PostgreSQL database: {e}")
    print("Please run create_database.py first to set up the database")
    sys.exit(1)

app.include_router(
    auth_router,
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    dishes_router,
    tags=["Dishes"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    orders_router,
    tags=["Orders"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    pages_router,
    tags=["Pages"],
    responses={404: {"description": "Not found"}},
)

@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": "Welcome to Restaurant API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  
        workers=1
    )