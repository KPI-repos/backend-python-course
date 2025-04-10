import hashlib
from app.database import get_database, get_mongo_client
from bson.objectid import ObjectId

def init_test_data():
    """Initialize test users and sample dishes in the MongoDB database"""
    client = get_mongo_client()
    db = get_database(client)
    
    try:
        users_collection = db['users']
        dishes_collection = db['dishes']
        
        admin = users_collection.find_one({'login': 'admin'})
        if not admin:
            admin_password = hashlib.sha256('admin'.encode()).hexdigest()
            users_collection.insert_one({
                'login': 'admin',
                'email': 'admin@example.com',
                'password': admin_password,
                'role': 'admin'
            })

        customer = users_collection.find_one({'login': 'customer'})
        if not customer:
            customer_password = hashlib.sha256('customer'.encode()).hexdigest()
            users_collection.insert_one({
                'login': 'customer',
                'email': 'customer@example.com',
                'password': customer_password,
                'role': 'customer'
            })

        sample_dishes = [
            {
                "title": "Піца Маргарита",
                "description": "Традиційна італійська піца з томатним соусом та моцарелою",
                "price": 200.00
            },
            {
                "title": "Борщ український",
                "description": "Класичний український борщ з буряком, м'ясом та сметаною",
                "price": 150.00
            },
            {
                "title": "Суші Філадельфія",
                "description": "Роли з лососем, сиром Філадельфія та огірком",
                "price": 250.00
            }
        ]

        for dish_data in sample_dishes:
            existing_dish = dishes_collection.find_one({'title': dish_data["title"]})
            if not existing_dish:
                dishes_collection.insert_one(dish_data)

        print("Test data initialized successfully")
        
    except Exception as e:
        print(f"Error initializing test data: {e}")
    finally:
        client.close()