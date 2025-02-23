import hashlib
from app.database import SessionLocal
from app.models import User, Dish

def init_test_data():
    """Initialize test users and sample dishes in the database"""
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.login == 'admin').first()
        if not admin:
            admin_password = hashlib.sha256('admin'.encode()).hexdigest()
            admin = User(
                login='admin',
                email='admin@example.com',
                password=admin_password,
                role='admin'
            )
            db.add(admin)

        customer = db.query(User).filter(User.login == 'customer').first()
        if not customer:
            customer_password = hashlib.sha256('customer'.encode()).hexdigest()
            customer = User(
                login='customer',
                email='customer@example.com',
                password=customer_password,
                role='customer'
            )
            db.add(customer)

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
            existing_dish = db.query(Dish).filter(Dish.title == dish_data["title"]).first()
            if not existing_dish:
                dish = Dish(**dish_data)
                db.add(dish)

        db.commit()
        print("Test data initialized successfully")
        
    except Exception as e:
        db.rollback()
        print(f"Error initializing test data: {e}")
    finally:
        db.close()