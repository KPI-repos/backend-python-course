import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database"""
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = ON")
        print(f"Connected to SQLite database: {db_file}")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite database: {e}")
        return None

def create_tables(conn):
    """Create required tables in the SQLite database"""
    try:
        cursor = conn.cursor()
        
        # Create User table with role
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS User (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'customer'))
            );
        """)

        # Create Dishes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Dishes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL
            );
        """)

        # Create Orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                dish_id INTEGER NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES User (id),
                FOREIGN KEY (dish_id) REFERENCES Dishes (id)
            );
        """)

        conn.commit()
        print("Tables created successfully")

    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

def insert_sample_data(conn):
    """Insert sample data into the database"""
    try:
        cursor = conn.cursor()

        # Insert admin user
        cursor.execute("""
            INSERT OR IGNORE INTO User (login, email, password, role)
            VALUES (?, ?, ?, ?);
        """, ('admin', 'admin@example.com', 
              '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918',  # admin
              'admin'))

        # Insert sample customer
        cursor.execute("""
            INSERT OR IGNORE INTO User (login, email, password, role)
            VALUES (?, ?, ?, ?);
        """, ('customer', 'customer@example.com',
              '91fe0a703ef5d41c784e5ef2c7cc306a5e208c6f5719b89f14c89968355c161a',  # customer
              'customer'))

        # Insert sample dishes
        dishes = [
            ("Піца Маргарита", "Традиційна італійська піца з томатним соусом та моцарелою", 200.00),
            ("Борщ український", "Класичний український борщ з буряком, м'ясом та сметаною", 150.00),
            ("Суші Філадельфія", "Роли з лососем, сиром Філадельфія та огірком", 250.00)
        ]
        cursor.executemany("""
            INSERT OR IGNORE INTO Dishes (title, description, price)
            VALUES (?, ?, ?);
        """, dishes)

        conn.commit()
        print("Sample data inserted successfully")

    except sqlite3.Error as e:
        print(f"Error inserting sample data: {e}")

def init_database():
    """Initialize the database with tables and sample data"""
    database = "shop.db"
    conn = create_connection(database)
    
    if conn is not None:
        create_tables(conn)
        insert_sample_data(conn)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

# Actually run the initialization
if __name__ == "__main__":
    init_database()