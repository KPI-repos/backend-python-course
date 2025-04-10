from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from app.database import get_mongo_client, get_database
from app import init_test_data
from app.routes import auth_router, dishes_router, orders_router, pages_router

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

client = get_mongo_client()
db = get_database(client)

collections = ['users', 'dishes', 'orders']
for collection in collections:
    if collection not in db.list_collection_names():
        db.create_collection(collection)

init_test_data()

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

@app.on_event("shutdown")
def shutdown_event():
    """
    Ensure MongoDB client is closed when the application shuts down
    """
    if 'client' in globals():
        client.close()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  
        workers=1
    )