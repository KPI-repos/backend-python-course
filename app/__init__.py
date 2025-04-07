import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import hashlib

DB_USER = "postgres"
DB_PASSWORD = "123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "restaurant"

def create_database():
    """Create the PostgreSQL database if it doesn't exist"""
    conn = psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DB_NAME,))
    exists = cursor.fetchone()
    
    if not exists:
        print(f"Creating database '{DB_NAME}'...")
        cursor.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"Database '{DB_NAME}' created successfully")
    else:
        print(f"Database '{DB_NAME}' already exists")
    
    cursor.close()
    conn.close()

def setup_tables():
    """Create the database tables"""
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        login VARCHAR(100) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(50) NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dishes (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        price DECIMAL(10, 2) NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        status VARCHAR(50) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id SERIAL PRIMARY KEY,
        order_id INTEGER REFERENCES orders(id),
        dish_id INTEGER REFERENCES dishes(id),
        quantity INTEGER NOT NULL,
        price DECIMAL(10, 2) NOT NULL
    )
    """)
    
    conn.commit()
    print("Database tables created successfully")
    
    init_test_data(conn)
    
    cursor.close()
    conn.close()

def init_test_data(conn):
    """Initialize test users and sample dishes in the database"""
    cursor = conn.cursor()
    
    cursor.execute("SELECT 1 FROM users WHERE login = 'admin'")
    admin_exists = cursor.fetchone()
    
    if not admin_exists:
        admin_password = hashlib.sha256('admin'.encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (login, email, password, role) VALUES (%s, %s, %s, %s)",
            ('admin', 'admin@example.com', admin_password, 'admin')
        )
    
    cursor.execute("SELECT 1 FROM users WHERE login = 'customer'")
    customer_exists = cursor.fetchone()
    
    if not customer_exists:
        customer_password = hashlib.sha256('customer'.encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (login, email, password, role) VALUES (%s, %s, %s, %s)",
            ('customer', 'customer@example.com', customer_password, 'customer')
        )
    
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
    
    for dish in sample_dishes:
        cursor.execute("SELECT 1 FROM dishes WHERE title = %s", (dish["title"],))
        dish_exists = cursor.fetchone()
        
        if not dish_exists:
            cursor.execute(
                "INSERT INTO dishes (title, description, price) VALUES (%s, %s, %s)",
                (dish["title"], dish["description"], dish["price"])
            )
    
    conn.commit()
    print("Test data initialized successfully")

if __name__ == "__main__":
    create_database()
    setup_tables()