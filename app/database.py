from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
from typing import Optional

MONGO_URI = "mongodb+srv://new-user1:new-user1@cluster0.obkkncb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "restaurant"

def get_mongo_client() -> MongoClient:

    try:
        client = MongoClient(
            MONGO_URI, 
            tlsCAFile=certifi.where(), 
            server_api=ServerApi('1')
        )
        # Verify connection
        client.admin.command('ping')
        return client
    except Exception as e:
        raise ConnectionError(f"Failed to connect to MongoDB: {e}")

def get_database(client: Optional[MongoClient] = None) -> object:
   
    if client is None:
        client = get_mongo_client()
    return client[DATABASE_NAME]

def get_db():
  
    client = None
    try:
        client = get_mongo_client()
        db = get_database(client)
        yield db
    finally:
        if client:
            client.close()