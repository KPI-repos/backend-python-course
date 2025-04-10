from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi

try:
    cluster = MongoClient("mongodb+srv://new-user1:new-user1@cluster0.obkkncb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", tlsCAFile=certifi.where(), server_api=ServerApi('1'))
    
    db = cluster['restaurant']
    collection = db['restaurant']
    
    server_info = cluster.server_info()
    
    print("SUCCESS: Successfully connected to MongoDB!")
    print(f"Server info: {server_info['version']}")
    print(f"Database: {db.name}")
    print(f"Collection: {collection.name}")
    
    doc_count = collection.count_documents({})
    print(f"Number of documents in collection: {doc_count}")
    
finally:
    if 'cluster' in locals():
        cluster.close()
        print("Connection closed.")