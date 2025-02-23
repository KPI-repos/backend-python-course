from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from datetime import datetime
import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.append(str(Path(__file__).parent))

from app.database import engine
from app import init_test_data
from app.models.tables import Base
from app.routes import auth_router, dishes_router, orders_router, pages_router

# Create the FastAPI app
app = FastAPI(
    title="Restaurant API",
    description="API for restaurant management system",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="public/static"), name="static")

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize test data
init_test_data()

# Include routers
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

# Root endpoint
@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": "Welcome to Restaurant API",
        "version": "1.0.0",
        "status": "running"
    }

# Health check endpoint
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
        reload=True,  # Enable auto-reload
        workers=1
    )